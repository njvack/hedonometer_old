# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OutgoingTextMessage'
        db.create_table('texter_outgoingtextmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['texter.Experiment'])),
            ('from_phone', self.gf('texter.models.PhoneNumberField')(max_length=255)),
            ('to_phone', self.gf('texter.models.PhoneNumberField')(max_length=255)),
            ('message_text', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('send_scheduled_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('texter', ['OutgoingTextMessage'])

        # Adding model 'IncomingTextMessage'
        db.create_table('texter_incomingtextmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['texter.Experiment'])),
            ('from_phone', self.gf('texter.models.PhoneNumberField')(max_length=255)),
            ('to_phone', self.gf('texter.models.PhoneNumberField')(max_length=255)),
            ('message_text', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('received_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('texter', ['IncomingTextMessage'])


    def backwards(self, orm):
        
        # Deleting model 'OutgoingTextMessage'
        db.delete_table('texter_outgoingtextmessage')

        # Deleting model 'IncomingTextMessage'
        db.delete_table('texter_incomingtextmessage')


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
            'backend': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['texter.Backend']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_slug': ('django.db.models.fields.SlugField', [], {'default': "'fbkfzrdqhk'", 'unique': 'True', 'max_length': '10', 'db_index': 'True'})
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
        }
    }

    complete_apps = ['texter']
