# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Experiment'
        db.create_table('texter_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url_slug', self.gf('django.db.models.fields.SlugField')(max_length=10, db_index=True)),
        ))
        db.send_create_signal('texter', ['Experiment'])


    def backwards(self, orm):
        
        # Deleting model 'Experiment'
        db.delete_table('texter_experiment')


    models = {
        'texter.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_slug': ('django.db.models.fields.SlugField', [], {'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['texter']
