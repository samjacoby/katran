# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Entry.secondary_content'
        db.add_column('entries_entry', 'secondary_content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='secondary_content', null=True, to=orm['cms.Placeholder']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Entry.secondary_content'
        db.delete_column('entries_entry', 'secondary_content_id')


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
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'list_display'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'entry_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'secondary_content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secondary_content'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'sidebar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sidebar'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['entries']
