# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TropoBackend'
        db.delete_table('texter_tropobackend')


    def backwards(self, orm):
        
        # Adding model 'TropoBackend'
        db.create_table('texter_tropobackend', (
            ('phone_number', self.gf('texter.models.PhoneNumberField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('session_request_url', self.gf('django.db.models.fields.URLField')(default='https://api.tropo.com/1.0/sessions', max_length=255)),
            ('sms_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('texter', ['TropoBackend'])


    models = {
        'texter.backend': {
            'Meta': {'object_name': 'Backend'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delegate_classname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'delegate_pk': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'texter.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Backend']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_slug': ('django.db.models.fields.SlugField', [], {'max_length': '10', 'db_index': 'True'})
        }
    }

    complete_apps = ['texter']
