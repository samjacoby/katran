# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Designer.sponsor'
        db.delete_column('stamps_designer', 'sponsor_id')

        # Adding M2M table for field sponsor on 'Designer'
        db.create_table('stamps_designer_sponsor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('designer', models.ForeignKey(orm['stamps.designer'], null=False)),
            ('sponsor', models.ForeignKey(orm['stamps.sponsor'], null=False))
        ))
        db.create_unique('stamps_designer_sponsor', ['designer_id', 'sponsor_id'])

        # Deleting field 'Family.sponsor'
        db.delete_column('stamps_family', 'sponsor_id')

        # Adding M2M table for field sponsor on 'Family'
        db.create_table('stamps_family_sponsor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('family', models.ForeignKey(orm['stamps.family'], null=False)),
            ('sponsor', models.ForeignKey(orm['stamps.sponsor'], null=False))
        ))
        db.create_unique('stamps_family_sponsor', ['family_id', 'sponsor_id'])

        # Deleting field 'Stamp.sponsor'
        db.delete_column('stamps_stamp', 'sponsor_id')

        # Adding M2M table for field sponsor on 'Stamp'
        db.create_table('stamps_stamp_sponsor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stamp', models.ForeignKey(orm['stamps.stamp'], null=False)),
            ('sponsor', models.ForeignKey(orm['stamps.sponsor'], null=False))
        ))
        db.create_unique('stamps_stamp_sponsor', ['stamp_id', 'sponsor_id'])


    def backwards(self, orm):
        
        # Adding field 'Designer.sponsor'
        db.add_column('stamps_designer', 'sponsor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stamps.Sponsor'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field sponsor on 'Designer'
        db.delete_table('stamps_designer_sponsor')

        # Adding field 'Family.sponsor'
        db.add_column('stamps_family', 'sponsor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stamps.Sponsor'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field sponsor on 'Family'
        db.delete_table('stamps_family_sponsor')

        # Adding field 'Stamp.sponsor'
        db.add_column('stamps_stamp', 'sponsor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stamps.Sponsor'], null=True, blank=True), keep_default=False)

        # Removing M2M table for field sponsor on 'Stamp'
        db.delete_table('stamps_stamp_sponsor')


    models = {
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'stamps.designer': {
            'Meta': {'ordering': "['normalized_name']", 'object_name': 'Designer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'info': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'sponsor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['stamps.Sponsor']", 'null': 'True', 'blank': 'True'}),
            'stamp_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'stamps.family': {
            'Meta': {'ordering': "['order']", 'object_name': 'Family'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'families'", 'to': "orm['stamps.Designer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'sponsor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['stamps.Sponsor']", 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'stamps.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stamps.stamp': {
            'Meta': {'ordering': "['order']", 'object_name': 'Stamp'},
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
            'sponsor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['stamps.Sponsor']", 'null': 'True', 'blank': 'True'}),
            'url_override': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['stamps']
