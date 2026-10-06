import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=11)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('endereco', models.CharField(max_length=200)),
                ('numero', models.CharField(max_length=10)),
                ('bairro', models.CharField(blank=True, default='', max_length=100)),
                ('cidade', models.CharField(blank=True, default='', max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='alunos/')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Esporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='esportes/')),
                ('descricao', models.TextField(blank=True)),
                ('categoria', models.CharField(blank=True, max_length=100)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=11)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='professores/')),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('SEG', 'Segunda-feira'), ('TER', 'Terça-feira'), ('QUA', 'Quarta-feira'), ('QUI', 'Quinta-feira'), ('SEX', 'Sexta-feira'), ('SAB', 'Sábado'), ('DOM', 'Domingo')], max_length=3)),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('ativo', models.BooleanField(default=True)),
                ('esporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='gestao.esporte')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='gestao.professor')),
            ],
            options={
                'ordering': ['dia_semana', 'hora_inicio'],
            },
        ),
        migrations.CreateModel(
            name='MatriculaHorario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('data_matricula', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas_horarios', to='gestao.aluno')),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas_alunos', to='gestao.horario')),
            ],
        ),
        migrations.CreateModel(
            name='Participacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_participacao', models.DateField()),
                ('presente', models.BooleanField(default=False)),
                ('data_registro', models.DateTimeField(auto_now_add=True)),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participacoes', to='gestao.matriculahorario')),
            ],
            options={
                'ordering': ['-data_participacao'],
            },
        ),
        migrations.AddConstraint(
            model_name='matriculahorario',
            constraint=models.UniqueConstraint(fields=('aluno', 'horario'), name='unico_aluno_horario'),
        ),
        migrations.AddConstraint(
            model_name='participacao',
            constraint=models.UniqueConstraint(fields=('matricula', 'data_participacao'), name='unico_matricula_data'),
        ),
    ]
