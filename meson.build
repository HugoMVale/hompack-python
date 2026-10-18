project(
  'hompack',
  ['fortran'],
  version : '0.0.1',
  meson_version: '>=1.5.0',
  default_options: [
    'buildtype=release',
    'b_ndebug=if-release',
    'hompack:blas_option=refblas',
    'hompack:build_shared=true',
    'hompack:build_examples=false',
    'hompack:build_tests=false',
  ],
)

# python
python = import('python').find_installation(pure: false)

# hompack (from subprojects)
hompack_lib = subproject('hompack').get_variable('hompack_lib')

if host_machine.system() == 'windows'
  hompack_so_name = 'hompack.dll'
elif host_machine.system() == 'darwin'
  hompack_so_name = 'libhompack.dylib'
else
  hompack_so_name = 'libhompack.so'
endif

# shared library for ctypes, copied into the package dir (subproject installs to libdir)
custom_target(
  'hompack_shared_copy',
  command: [
    python,
    '-c',
    'import shutil, sys; shutil.copy2(sys.argv[1], sys.argv[2])',
    hompack_lib,
    '@OUTPUT@',
  ],
  output: hompack_so_name,
  install: true,
  install_dir: join_paths(python.get_install_dir(), 'hompack'),
)

# scaffold
python.install_sources(
  [
  'src/hompack/__init__.py',
  ],
  subdir: 'hompack'
)

