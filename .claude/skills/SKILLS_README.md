# 🎯 Skills System - SaaS Factory

**Skills** son carpetas con instrucciones que enseñan a Claude cómo hacer tareas especializadas. Son el corazón de la extensibilidad en Claude Code.

## 📚 Estructura Recomendada por Anthropic

```
skill-name/
├── SKILL.md              # Requerido: Metadatos + Instrucciones
├── scripts/              # Opcional: Código ejecutable
│   ├── helper.py
│   └── processor.sh
├── references/           # Opcional: Documentación de referencia
│   ├── api_docs.md
│   └── schemas.md
└── assets/              # Opcional: Recursos de salida
    ├── templates/
    └── icons/
```

## SKILL.md - Estructura Mínima

```yaml
---
name: skill-name              # Identificador único (lowercase, hyphens)
description: What this skill  # Cuándo y por qué usarlo
                does and when
license: MIT                  # (Opcional)
---

# Skill Title

## Purpose
Qué hace el skill.

## When to Use
Cuándo Claude debería activarlo.

## How to Use
Instrucciones paso a paso.
```

## ✅ Principios de Anthropic

### Progressive Disclosure (Carga Eficiente)
1. **Metadata** (~100 palabras) - Siempre en contexto
2. **SKILL.md** (<5k palabras) - Cuando se activa
3. **Resources** (unlimited) - Bajo demanda

### Organización

| Carpeta | Cuándo Usar | Formato |
|---------|------------|---------|
| **scripts/** | Código reutilizable | .py, .sh, .js |
| **references/** | Documentación >5k | .md, .txt |
| **assets/** | Recursos de salida | .html, .png, .ttf |

### Naming Conventions

- **Skills**: `kebab-case` (skill-creator)
- **Scripts**: `action_noun.py` (create_skill.py)
- **References**: `descriptive_name.md` (api_docs.md)

## 🛠️ Tools Incluidos

### skill-creator
Herramienta para crear nuevos skills en SaaS Factory.

**Ubicación**: `.claude/skills/skill-creator/`

**Scripts**:
- `init_skill.py` - Crear nueva skill
- `quick_validate.py` - Validar skill
- `package_skill.py` - Empaquetar para distribución

**Uso**:
```bash
python init_skill.py my-skill
python quick_validate.py ./my-skill
python package_skill.py ./my-skill
```

---

## 🎯 **Portfolio Skills - MVP Collection**

Skills especializadas para crear portafolios profesionales de desarrolladores con contenido optimizado, SEO, diseño profesional y rendimiento excepcional.

### 📝 **portfolio-content-writer**
Genera contenido profesional para portafolios de desarrolladores.

**Propósito**: Transforma logros técnicos en narrativas de negocio, crea descripciones de proyectos atractivas y produce contenido optimizado para SEO.

**Cuando usar**:
- Construir nuevos portafolios desde cero
- Actualizar portafolios existentes
- Crear descripciones de proyectos desde READMEs y commits
- Escribir blog posts técnicos
- Aplicaciones a trabajos y propuestas freelance

**Scripts incluidos**:
- `content_generator.py` - Análisis de proyectos y generación de contenido
- `template_engine.py` - Sistema de plantillas personalizables
- `impact_analyzer.py` - Análisis de impacto y métricas de negocio

**Uso**:
```bash
python scripts/content_generator.py analyze --project-path ./your-project
python scripts/template_engine.py generate --template about_me --style technical
```

### 🔍 **seo-optimizer**
Optimización SEO completa para portafolios de desarrolladores.

**Propósito**: Mejora visibilidad en buscadores y atrae recruiters con estrategias SEO específicas para la industria tech.

**Cuando usar**:
- Audit SEO completo de portafolios
- Optimización para búsquedas de recruiters
- Investigación de keywords técnicas
- Optimización de meta tags y structured data
- Análisis competitivo

**Scripts incluidos**:
- `seo_auditor.py` - Auditor SEO completo
- `keyword_researcher.py` - Investigador de palabras clave
- `meta_generator.py` - Generador de meta tags optimizados
- `schema_generator.py` - Generador de datos estructurados

**Uso**:
```bash
python scripts/seo_auditor.py ./portfolio --url https://yourportfolio.com
python scripts/keyword_researcher.py --technology "React" --location "Remote"
```

### 🎨 **portfolio-design-system**
Sistema de diseño profesional para portafolios consistentes.

**Propósito**: Crea sistemas de diseño completos con component libraries, themes y patrones responsive para portafolios impresionantes.

**Cuando usar**:
- Diseñar portafolios visualmente profesionales
- Crear component libraries consistentes
- Implementar dark/light themes
- Garantizar accesibilidad WCAG
- Optimizar para mobile y desktop

**Scripts incluidos**:
- `theme_generator.py` - Generador de themes profesionales
- `component_scaffolder.py` - Creador de componentes React
- `design_token_validator.py` - Validador de sistemas de diseño
- `accessibility_checker.py` - Auditor de accesibilidad

**Uso**:
```bash
python scripts/theme_generator.py --personality innovative --output ./themes
python scripts/component_scaffolder.py --type ProjectCard --name MyPortfolio
```

### ⚡ **portfolio-performance-optimizer**
Optimización extrema de rendimiento para portafolios ultrarrápidos.

**Propósito**: Asegura Core Web Vitals perfectos, tiempos de carga mínimos y experiencia de usuario excepcional.

**Cuando usar**:
- Optimizar rendimiento de portafolios existentes
- Alcanzar Lighthouse scores 95+
- Implementar Core Web Vitals óptimos
- Optimizar bundle size y loading time
- Configurar caching strategies

**Scripts incluidos**:
- `performance_auditor.py` - Auditor completo de rendimiento
- `bundle_optimizer.py` - Optimización de Next.js 16 y Turbopack
- `image_optimizer.py` - Optimización de imágenes y assets
- `service_worker_generator.py` - Generador de caching strategies

**Uso**:
```bash
python scripts/performance_auditor.py ./portfolio --lighthouse
python scripts/bundle_optimizer.py ./portfolio --optimize
```

---

## 🔄 **Flujo de Trabajo Completo para Portafolios**

### **Workflow MVP**:
```bash
# 1. Generar contenido profesional
skill: "portfolio-content-writer"

# 2. Optimizar para recruiters y SEO
skill: "seo-optimizer"

# 3. Aplicar diseño profesional
skill: "portfolio-design-system"

# 4. Optimizar rendimiento al máximo
skill: "portfolio-performance-optimizer"

# 5. Crear PRP integrado
/generar-prp "Portafolio Next.js 16 con las 4 skills de portfolio"

# 6. Ejecutar construcción completa
/ejecutar-prp "PRPs/portafolio-integrado.md"
```

### **Impacto Esperado**:
- ✅ **Contenido Profesional**: Transforma código en valor de negocio
- ✅ **SEO Optimizado**: 2-4x visibilidad para recruiters
- ✅ **Diseño Impecable**: UI/UX a nivel enterprise
- ✅ **Rendimiento Extremo**: Lighthouse 95+, loading < 1s

## 📖 Referencias Recomendadas

- [Agent Skills Spec](https://docs.anthropic.com/) - Especificación formal
- [Skill Creator Guide](https://docs.anthropic.com/) - Guía completa
- [Best Practices](https://docs.anthropic.com/) - Patrones probados

## 🎯 Flujo de Creación

1. **Inicializar**: `python init_skill.py my-skill`
2. **Desarrollar**: Editar SKILL.md + agregar scripts/references/assets
3. **Validar**: `python quick_validate.py ./my-skill`
4. **Empaquetar**: `python package_skill.py ./my-skill`
5. **Instalar**: `/plugin install my-skill.zip`
6. **Usar**: Mencionar el skill en conversación

## 📝 Checklist para Crear un Skill

```
□ SKILL.md con YAML frontmatter válido
  □ name (lowercase, hyphens)
  □ description (3-5 oraciones)

□ Contenido bien organizado
  □ SKILL.md <5k palabras
  □ scripts/ para código reutilizable
  □ references/ para documentación
  □ assets/ para recursos

□ Scripts listos
  □ Tienen --help
  □ Incluyen docstrings
  □ Manejan errores

□ Validación
  □ python quick_validate.py ./skill-name
  □ Resultado: ✓ All OK!

□ Empaquetado
  □ python package_skill.py ./skill-name
  □ Resultado: skill-name.zip
```

## 💡 Ejemplo: Skill Simple

```
my-skill/
├── SKILL.md
│   ---
│   name: my-skill
│   description: Do X when Y happens
│   ---
│
│   # My Skill
│
│   ## Purpose
│   This skill...
│
│   ## How to Use
│   1. Step one
│   2. Step two
│
├── scripts/
│   └── processor.py
│
└── references/
    └── api_docs.md
```

## 🚀 Próximos Pasos

1. Usa `skill-creator` para crear nuevos skills
2. Sigue estos principios para mantener consistencia
3. Valida siempre antes de distribuir
4. Documenta claramente para otros desarrolladores

---

*Sistema de Skills estandardizado para SaaS Factory*
*Basado en Anthropic Agent Skills Spec v1.0*
