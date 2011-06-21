# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Renaming column for 'Entry.content' to match new field type.
        db.rename_column('entries_entry', 'content', 'content_id')
        # Changing field 'Entry.content'
        db.alter_column('entries_entry', 'content_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['cms.Placeholder']))

        # Adding index on 'Entry', fields ['content']
        db.create_index('entries_entry', ['content_id'])

        # Renaming column for 'Entry.sidebar' to match new field type.
        db.rename_column('entries_entry', 'sidebar', 'sidebar_id')
        # Changing field 'Entry.sidebar'
        db.alter_column('entries_entry', 'sidebar_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['cms.Placeholder']))

        # Adding index on 'Entry', fields ['sidebar']
        db.create_index('entries_entry', ['sidebar_id'])


    def backwards(self, orm):
        
        # Removing index on 'Entry', fields ['sidebar']
        db.delete_index('entries_entry', ['sidebar_id'])

        # Removing index on 'Entry', fields ['content']
        db.delete_index('entries_entry', ['content_id'])

        # Renaming column for 'Entry.content' to match new field type.
        db.rename_column('entries_entry', 'content_id', 'content')
        # Changing field 'Entry.content'
        db.alter_column('entries_entry', 'content', self.gf('django.db.models.fields.TextField')(default=''))

        # Renaming column for 'Entry.sidebar' to match new field type.
        db.rename_column('entries_entry', 'sidebar_id', 'sidebar')
        # Changing field 'Entry.sidebar'
        db.alter_column('entries_entry', 'sidebar', self.gf('django.db.models.fields.TextField')(default=''))


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'entries.entry': {
            'Meta': {'ordering': "['-order']", 'object_name': 'Entry'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main_content'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'entry_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['entries.Image']", 'symmetrical': 'False', 'through': "orm['entries.EntryRelationship']", 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'sidebar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sidebar'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'entries.entryrelationship': {
            'Meta': {'object_name': 'EntryRelationship'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entries.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entries.Image']"}),
            'list_display': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        'entries.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['entries']
