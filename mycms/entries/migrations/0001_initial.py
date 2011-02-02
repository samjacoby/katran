# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('entries_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('src', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('entries', ['Image'])

        # Adding model 'Entry'
        db.create_table('entries_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('entry_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sidebar', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('display', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('entries', ['Entry'])

        # Adding model 'EntryRelationship'
        db.create_table('entries_entryrelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entries.Image'])),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entries.Entry'])),
            ('list_display', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('entries', ['EntryRelationship'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('entries_image')

        # Deleting model 'Entry'
        db.delete_table('entries_entry')

        # Deleting model 'EntryRelationship'
        db.delete_table('entries_entryrelationship')


    models = {
        'entries.entry': {
            'Meta': {'ordering': "['-order']", 'object_name': 'Entry'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'entry_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['entries.Image']", 'symmetrical': 'False', 'through': "orm['entries.EntryRelationship']", 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'sidebar': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'entries.entryrelationship': {
            'Meta': {'object_name': 'EntryRelationship'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entries.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entries.Image']"}),
            'list_display': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'entries.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['entries']
