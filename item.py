from flask import Blueprint, render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user
from .models import Item
from . import db
import os
from datetime import datetime

item = Blueprint('item', __name__)


@item.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        item = request.form['item']
        description = request.form['description']
        occurdate = request.form['occurdate']
        takentime = request.form['time']
#        photo = request.form.get('photo')
        
        if not item:
            flash('Item name is required!')
            return render_template('create.html')
        if not description:
            flash('Item description is required!')
            return render_template('create.html')
     #   if not photo:
      #      flash('Photo of the item is required!')
       #     return render_template('create.html')
        else:
            if occurdate:
                if not takentime:
                    conDate = datetime.strptime(occurdate, '%Y-%m-%d')
                    new_item = Item(item=item, description=description, occurdate=conDate)
                else:
                    conDate = datetime.strptime(occurdate, '%Y-%m-%d')
                    conTime = datetime.strptime(takentime, "%H:%M").time()
                    new_item = Item(item=item, description=description, occurdate=conDate, time=conTime)
            else:
                if takentime:
                    conTime = datetime.strptime(takentime, "%H:%M").time()
                    new_item = Item(item=item, description=description, time=conTime)

            db.session.add(new_item)
            db.session.commit()
            flash('"{}" is successfully listed!'.format(item))
            return redirect(url_for('main.home'))

    return render_template('create.html')

@item.route('/<int:item_id>/edit', methods=('GET','POST'))
@login_required
def edit(item_id):
    item = Item.query.filter_by(id=item_id).first()

    if request.method == 'POST':
        name = request.form['item']
        description = request.form['description']
        occurdate = request.form['occurdate']
        takentime = request.form['time']
        #photo = request.form.get('photo')
        try: 
            if not name:
                flash('Item name is required!')
                return render_template('edit.html', item=item)
            if not description:
                flash('Item description is required!')
                return render_template('edit.html', item=item)
            #if not photo:
                #flash('Photo of the item is required!')
                #return render_template('create.html')
            else:
                conDate = datetime.strptime(occurdate, '%Y-%m-%d')
                if takentime:
                    conTime = datetime.strptime(takentime, "%H:%M").time()
                
                updated = Item.query.get(item_id)
                if (name != updated.item):
                    updated.item = name
                if (description != updated.description):
                    updated.description = description
                if (conDate != updated.occurdate):
                    updated.occurdate = conDate
                if conTime and (conTime != updated.time):
                    updated.time = conTime

                db.session.commit()
                flash('"{}" is successfully edited!'.format(name))
                return redirect(url_for('main.home'))
        except ValueError:
            flash('The listing has not been edited!')
            return render_template('edit.html', item=item)

    else:
        return render_template('edit.html', item=item)


    return render_template('edit.html', item=item)


@item.route('/<int:listing_id>')
def listing(listing_id):
    listing = Item.query.filter_by(id=listing_id).first()
    return render_template('listing.html', listing=listing)

@item.route('/<int:item_id>/delete', methods=('POST',))
@login_required
def delete(item_id):
    item = Item.query.filter_by(id=item_id).first()

    ditem = Item.query.get(item_id)
    db.session.delete(ditem)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(item['item']))
    return redirect(url_for('main.home'))