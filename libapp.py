# -*- coding: utf-8 -*- 
# all the imports
from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, redirect, url_for, session, abort, render_template, flash, jsonify
from db import db_session, exists, get_or_create
from functools import wraps
from models import Book, Author
from paginator import Paginator # using pagintion from django package
import time
from wtforms_models import AuthorForm, BookForm

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
PAGIN = 25 # entries per page when paginating
CAT_VIEW = "books" # default category view
REGISTERED_MODELS=(Book,Author) # this list are used in search function to indicate where we want to search


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# decorator for wrapping views that requires authorization
def login_required(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if not session.get('logged_in'):
			flash('First you need to login')
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return wrapped

@app.after_request
def shutdown_session(response):
    db_session.remove()
    return response

@app.route('/')
def index():
	return redirect(url_for('show_entries',pagin = app.config['PAGIN'], page=1, view=app.config['CAT_VIEW'])) 

@app.route('/<any(books,authors):view>/<int:pagin>/<int:page>/')
def show_entries(view,pagin,page):
	if view =='books':
		entries_all = db_session.query(Book).all()
	else :
		entries_all = db_session.query(Author).all()
	paginator = Paginator(entries_all,pagin)
	try:
		entries = paginator.page(page)
	except PageNotAnInteger:
		entries = paginator.page(1)
	except EmptyPage:
		entries = paginator.page(paginator.num_pages)
	return	render_template('show_entries.html', entries=entries, entries_per_page=pagin,view_mode=view, config=app.config)

@app.route('/<any(book,author):view>/<int:item_id>/')
def show_entry(view,item_id):
	if view =='book':
		entry = db_session.query(Book).filter(Book.id==item_id).first()
	else :
		entry = db_session.query(Author).filter(Author.id==item_id).first()
	return	render_template('entry_page.html', entry=entry,view_mode=view)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
        	elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries',pagin = app.config['PAGIN'], page=1, view=app.config['CAT_VIEW']))
	return render_template('login.html', error=error)

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries',pagin = app.config['PAGIN'], page=1, view=app.config['CAT_VIEW']))

@app.route('/search/', methods=['GET'])
def search():
	results_dict = {}
	search_for=request.args.get('q')
	if search_for:
		for model in app.config['REGISTERED_MODELS']:
			results_dict[model.__plural__] = get_search_results(model,search_for)
	return	render_template('search_results.html',results_dict=results_dict, search_for=search_for)

def get_search_results(Model, query):	
	q = '%{0}%'.format(query)
	return db_session.query(Model).filter(Model.name.like(q)).all()

@app.route('/searchjson/', methods=['GET'])
def searchjson():
	results_dict = {
		'query':'',
		'suggestions':[]
		}
	# create list of models we need to look through from request args
	req_models = [request.args.get('model[%d]' % i) for i in range(5)]
	if request.is_xhr:
		search_for=request.args.get('query')
		results_dict['query'] = search_for
		if search_for:
			for model in app.config['REGISTERED_MODELS']:
				if model.__name__ in req_models:
					for item in get_search_results(model,search_for):
						results_dict['suggestions'].append(item.name)
		resp = jsonify(results_dict)
		resp.status_code = 200
		return resp
	resp = jsonify(results_dict)
	resp.status_code = 500
	return resp

@app.route('/admin/', methods=['GET'])
@login_required
def admin_panel():
	return redirect(url_for('admin_show_entries',pagin = app.config['PAGIN'], page=1, view=app.config['CAT_VIEW']))
	
@app.route('/admin/<any(books,authors):view>/<int:pagin>/<int:page>/',methods=['GET'])
@login_required
def admin_show_entries(view,pagin,page):
	if view =='books':
		entries_all = db_session.query(Book).all()
	else :
		entries_all = db_session.query(Author).all()
	paginator = Paginator(entries_all,pagin)
	try:
		entries = paginator.page(page)
	except PageNotAnInteger:
		entries = paginator.page(1)
	except EmptyPage:
		entries = paginator.page(paginator.num_pages)
	return	render_template('admin_entries.html', entries=entries, entries_per_page=pagin,view_mode=view, config=app.config)

@app.route('/admin/ajax/save/', methods=['POST'])
@login_required
def authors_edit():
	for model in app.config['REGISTERED_MODELS']:
		if model.__name__==request.form['name']:
			entry = db_session.query(model).filter(model.id==request.form['id']).first()
			entry_to_check = db_session.query(model).filter(model.name==request.form['value']).first()
	if entry:
		#check if entry with the same name already exists
		if entry_to_check and entry.id!=entry_to_check.id:
			return 'already exists in database', 500
		entry.name = request.form['value']
		db_session.commit()
		return entry.name, 200
	return 'failed', 500

@app.route('/admin/<any(books,authors):view>/add/', methods=['GET','POST']) 
@login_required
def add_entry(view): 
	if view=='books':
		form = BookForm(request.form)
	else:
		form = AuthorForm(request.form)
	if request.method == 'POST' and form.validate():
		if view=='books':
			entry = Book(name=form.name.data,description=form.description.data)
			for author in  form.authors.data:
				entry.authors.append(get_or_create(Author,name=author))
		else:
			entry = Author(str(form.name.data))
		db_session.add(entry)
		db_session.commit()		
		flash('%s successfuly added' % entry.name)
		return redirect(url_for('admin_show_entries',pagin = app.config['PAGIN'], page=1, view=view))
	flash('Add new entry to %s database' % view)
	return render_template('add_entry.html', form=form, view=view,mode='add')

@app.route('/admin/<any(books,authors):view>/edit/<int:id>/', methods=['GET','POST']) 
@login_required
def edit_entry(view, id): 
	entry = db_session.query(Book).filter(Book.id==id).first()
	form = BookForm(request.form,obj=entry)
	if request.method == 'POST' and form.validate():
		if view=='books':
			entry.authors = []
			for author in form.authors.data :
				entry.authors.append(get_or_create(Author,name=author))
			entry.name = form.name.data
			entry.description = form.description.data
		db_session.commit()		
		flash('%s successfuly have edited' % entry.name)
		return redirect(url_for('admin_show_entries',pagin = app.config['PAGIN'], page=1, view=view))
	flash('edited  entry to %s database' % view)
	return render_template('add_entry.html', form=form, view=view,entry=entry, mode="edit")


@app.route('/admin/<any(books,authors):view>/del/<int:id>/', methods=['GET','POST']) 
@login_required
def del_entry(view,id): 
	if view=='books':
		entry = db_session.query(Book).filter(Book.id==id).first()
	else:
		entry = db_session.query(Author).filter(Author.id==id).first()
	if entry:
		db_session.delete(entry)
		db_session.commit()		
		flash('%s successfuly removed from database' % entry.name)
	else:
		flash('No entry with id = %d' % id)
	return redirect(url_for('admin_show_entries',pagin = app.config['PAGIN'], page=1, view=view))

if __name__ == '__main__':
	app.run()

