# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('entries_image')

        # Deleting model 'EntryRelationship'
        db.delete_table('entries_entryrelationship')


    def backwards(self, orm):
        
        # Adding model 'Image'
        db.create_table('entries_image', (
            ('src', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('entries', ['Image'])

        # Adding model 'EntryRelationship'
        db.create_table('entries_entryrelationship', (
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entries.Image'])),
            ('list_display', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entries.Entry'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('entries', ['EntryRelationship'])


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'entries.entry': {
            'Meta': {'ordering': "['-order']", 'object_name': 'Entry'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secondary_content'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'list_display'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'entry_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'sidebar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sidebar'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['entries']
