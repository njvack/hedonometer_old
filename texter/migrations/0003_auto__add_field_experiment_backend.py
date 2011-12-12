# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Experiment.backend'
        db.add_column('texter_experiment', 'backend', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['texter.Backend']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Experiment.backend'
        db.delete_column('texter_experiment', 'backend_id')


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
        },
        'texter.tropobackend': {
            'Meta': {'object_name': 'TropoBackend'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'session_request_url': ('django.db.models.fields.URLField', [], {'default': "'https://api.tropo.com/1.0/sessions'", 'max_length': '255'}),
            'sms_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['texter']
