project('example_app', 'vala', 'c')

dependencies = [
    dependency('glib-2.0'),
    dependency('gobject-2.0'),
    dependency('gtk+-3.0'),
]

sources = files('main.vala')

executable(meson.project_name(), sources, dependencies: dependencies)
