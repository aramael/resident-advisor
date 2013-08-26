# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ZipCode'
        db.create_table(u'zipcodes_zipcode', (
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=6)),
            ('timezone', self.gf('django.db.models.fields.IntegerField')()),
            ('dst', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'zipcodes', ['ZipCode'])


    def backwards(self, orm):
        # Deleting model 'ZipCode'
        db.delete_table(u'zipcodes_zipcode')


    models = {
        u'zipcodes.zipcode': {
            'Meta': {'object_name': 'ZipCode'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dst': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'})
        }
    }

    complete_apps = ['zipcodes']