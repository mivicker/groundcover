# Generated by Django 4.0.4 on 2022-05-22 15:24

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail_color_panel.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveEntry',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='logo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='socials',
            field=wagtail.fields.StreamField([('account', wagtail.blocks.StructBlock([('platform', wagtail.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('invert_image', wagtail.images.blocks.ImageChooserBlock()), ('url', wagtail.blocks.CharBlock())]))], blank=True, use_json_field=None),
        ),
        migrations.AddField(
            model_name='homepage',
            name='theme_color',
            field=wagtail_color_panel.fields.ColorField(default='#FF0000', max_length=7),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='GetInvolved',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='TeamPage',
            fields=[
                ('staticpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.staticpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('home.staticpage',),
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('bio', models.TextField()),
                ('author_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('lede', models.CharField(max_length=1024)),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], blank=True, null=True, use_json_field=None)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.writer')),
                ('lead_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
