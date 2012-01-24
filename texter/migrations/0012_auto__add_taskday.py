# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TaskDay'
        db.create_table('texter_taskday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['texter.Participant'])),
            ('task_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('earliest_contact', self.gf('django.db.models.fields.DateTimeField')()),
            ('latest_contact', self.gf('django.db.models.fields.DateTimeField')()),
            ('_run_state', self.gf('django.db.models.fields.CharField')(default='waiting', max_length=255)),
        ))
        db.send_create_signal('texter', ['TaskDay'])


    def backwards(self, orm):
        
        # Deleting model 'TaskDay'
        db.delete_table('texter_taskday')


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
        'texter.dummybackend': {
            'Meta': {'object_name': 'DummyBackend'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'handle_request_calls': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_message_calls': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'texter.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Backend']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'experiment_length_days': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_slug': ('django.db.models.fields.SlugField', [], {'default': "'tcgbbqfvfj'", 'unique': 'True', 'max_length': '10', 'db_index': 'True'})
        },
        'texter.incomingtextmessage': {
            'Meta': {'object_name': 'IncomingTextMessage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Experiment']"}),
            'from_phone': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_text': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'received_at': ('django.db.models.fields.DateTimeField', [], {}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'to_phone': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'texter.outgoingtextmessage': {
            'Meta': {'object_name': 'OutgoingTextMessage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Experiment']"}),
            'from_phone': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_text': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'send_scheduled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'to_phone': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'texter.participant': {
            'Meta': {'unique_together': "(['experiment', 'phone_number'],)", 'object_name': 'Participant'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'normal_earliest_message_time': ('django.db.models.fields.TimeField', [], {'default': "'9:00'"}),
            'normal_latest_message_time': ('django.db.models.fields.TimeField', [], {'default': "'21:00'"}),
            'phone_number': ('texter.models.PhoneNumberField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'stopped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'texter.taskday': {
            'Meta': {'object_name': 'TaskDay'},
            '_run_state': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'earliest_contact': ('django.db.models.fields.DateTimeField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_contact': ('django.db.models.fields.DateTimeField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Participant']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'task_date': ('django.db.models.fields.DateField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['texter']
