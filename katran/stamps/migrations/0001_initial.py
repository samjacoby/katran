# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Sponsor'
        db.create_table('stamps_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stamps', ['Sponsor'])

        # Adding model 'Designer'
        db.create_table('stamps_designer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('normalized_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('stamp_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_navigation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('info', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
        ))
        db.send_create_signal('stamps', ['Designer'])

        # Adding model 'Family'
        db.create_table('stamps_family', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('designer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='families', to=orm['stamps.Designer'])),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_navigation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('stamps', ['Family'])

        # Adding model 'Stamp'
        db.create_table('stamps_stamp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('family', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stamps', to=orm['stamps.Family'])),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_navigation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url_override', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('picture', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stamp_picture', null=True, to=orm['cms.Placeholder'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('info', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stamp_info', null=True, to=orm['cms.Placeholder'])),
            ('footer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stamp_footer', null=True, to=orm['cms.Placeholder'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('stamps', ['Stamp'])


    def backwards(self, orm):
        
        # Deleting model 'Sponsor'
        db.delete_table('stamps_sponsor')

        # Deleting model 'Designer'
        db.delete_table('stamps_designer')

        # Deleting model 'Family'
        db.delete_table('stamps_family')

        # Deleting model 'Stamp'
        db.delete_table('stamps_stamp')


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
            'Meta': {'object_name': 'Designer'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'stamp_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'stamps.family': {
            'Meta': {'object_name': 'Family'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'families'", 'to': "orm['stamps.Designer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'})
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
            'Meta': {'object_name': 'Stamp'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamps'", 'to': "orm['stamps.Family']"}),
            'footer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamp_footer'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamp_info'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stamp_picture'", 'null': 'True', 'to': "orm['cms.Placeholder']"}),
            'url_override': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'blank': 'True'})
        }
    }

    complete_apps = ['stamps']
