# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.cover'
        db.add_column('entries_entry', 'cover', self.gf('django.db.models.fields.related.ForeignKey')(related_name='list_display', null=True, to=orm['cms.Placeholder']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entry.cover'
        db.delete_column('entries_entry', 'cover_id')


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'entries.entry': {
            'Meta': {'ordering': "['-order']", 'object_name': 'Entry'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'detail'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'list_display'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
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
