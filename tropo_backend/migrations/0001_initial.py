# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TropoBackend'
        db.create_table('tropo_backend_tropobackend', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sms_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('session_request_url', self.gf('django.db.models.fields.URLField')(default='https://api.tropo.com/1.0/sessions', max_length=255)),
            ('phone_number', self.gf('texter.models.PhoneNumberField')(max_length=255)),
        ))
        db.send_create_signal('tropo_backend', ['TropoBackend'])


    def backwards(self, orm):
        
        # Deleting model 'TropoBackend'
        db.delete_table('tropo_backend_tropobackend')


    models = {
        'tropo_backend.tropobackend': {
            'Meta': {'object_name': 'TropoBackend'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'session_request_url': ('django.db.models.fields.URLField', [], {'default': "'https://api.tropo.com/1.0/sessions'", 'max_length': '255'}),
            'sms_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tropo_backend']
