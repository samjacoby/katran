# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Designer.display_name'
        db.delete_column('stamps_designer', 'display_name')

        # Adding field 'Designer.name'
        db.add_column('stamps_designer', 'name', self.gf('django.db.models.fields.CharField')(default='Display Name', max_length=100), keep_default=False)

        # Adding unique constraint on 'Family', fields ['designer', 'order']
        db.create_unique('stamps_family', ['designer_id', 'order'])

        # Changing field 'Stamp.value'
        db.alter_column('stamps_stamp', 'value', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Adding unique constraint on 'Stamp', fields ['order', 'family']
        db.create_unique('stamps_stamp', ['order', 'family_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Stamp', fields ['order', 'family']
        db.delete_unique('stamps_stamp', ['order', 'family_id'])

        # Removing unique constraint on 'Family', fields ['designer', 'order']
        db.delete_unique('stamps_family', ['designer_id', 'order'])

        # Adding field 'Designer.display_name'
        db.add_column('stamps_designer', 'display_name', self.gf('django.db.models.fields.CharField')(default='', max_length=60, blank=True), keep_default=False)

        # Deleting field 'Designer.name'
        db.delete_column('stamps_designer', 'name')

        # Changing field 'Stamp.value'
        db.alter_column('stamps_stamp', 'value', self.gf('django.db.models.fields.CharField')(max_length=30))


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stamps.designer': {
            'Meta': {'ordering': "['normalized_name']", 'object_name': 'Designer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'stamp_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'stamps.family': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('designer', 'order'),)", 'object_name': 'Family'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'families'", 'to': "orm['stamps.Designer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'stamps.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'stamps.stamp': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('family', 'order'),)", 'object_name': 'Stamp'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamps'", 'to': "orm['stamps.Family']"}),
            'footer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamp_footer'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamp_info'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url_override': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['stamps']
