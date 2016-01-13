// Generated on 2015-11-27 using generator-angular 0.14.0
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) {

	// Time how long tasks take. Can help when optimizing build times
	require('time-grunt')(grunt);

	// Automatically load required Grunt tasks
	require('jit-grunt')(grunt, {
		useminPrepare: 'grunt-usemin',
		ngtemplates: 'grunt-angular-templates',
		cdnify: 'grunt-google-cdn'
	});

	// Mod rewrite
	var modRewrite = require('connect-modrewrite');

	// Configurable paths for the application
	var appConfig = require('./app/config.js');
	appConfig.app = require('./bower.json').appPath || 'app';
	appConfig.dist = 'dist';

	// Define the configuration for all the tasks
	grunt.initConfig({

		// Project settings
		birda: appConfig,

		// Watches files for changes and runs tasks based on the changed files
		watch: {
			bower: {
				files: ['bower.json'],
				tasks: ['wiredep']
			},
			js: {
				files: ['<%= birda.app %>/scripts/{,*/}*.js'],
				tasks: ['newer:jshint:all', 'newer:jscs:all'],
				options: {
					livereload: '<%= connect.options.livereload %>'
				}
			},
			jsTest: {
				files: ['test/spec/{,*/}*.js'],
				tasks: ['newer:jshint:test', 'newer:jscs:test', 'karma']
			},
			compass: {
				files: ['<%= birda.app %>/styles/{,*/}*.{scss,sass}'],
				tasks: ['compass:server', 'postcss:server']
			},
			gruntfile: {
				files: ['Gruntfile.js']
			},
			livereload: {
				options: {
					livereload: '<%= connect.options.livereload %>'
				},
				files: [
					'<%= birda.app %>/{,*/}*.html',
					'.tmp/styles/{,*/}*.css',
					'<%= birda.app %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}'
				]
			}
		},

		// The actual grunt server settings
		connect: {
			options: {
				port: '<%= birda.port %>',
				// Change this to '0.0.0.0' to access the server from outside.
				//hostname: 'localhost',
				hostname: '<%= birda.hostname %>',
				livereload: '<%= birda.portLivereload %>',
				middleware: function (connect, options, middlewares) {

					return [
						// CORS settings
						//function (req, res, next) {
						//	res.setHeader('Access-Control-Allow-Origin', '*');
						//	res.setHeader('Access-Control-Allow-Methods', '*');
						//	//a console.log('foo') here is helpful to see if it runs
						//	return next();
						//},

						// Mapping every filetype is unconfortable and error-prone
						//modRewrite(['!\\.html|\\.js|\\.svg|\\.css|\\.png|\\.ico$ /index.html [L]']),
						modRewrite(['!\\.[a-zA-Z0-9]+$ /index.html [L]']),
						connect.static('.tmp'),
						connect().use(
							'/bower_components',
							connect.static('./bower_components')
						),
						connect().use(
							'/app/styles',
							connect.static('./app/styles')
						),
						connect.static(appConfig.app)
					];
				}
			},
			livereload: {
				options: {
					open: true
				}
			},
			test: {
				options: {
					port: '<%= birda.portDev %>',
					middleware: function (connect) {
						return [
							connect.static('.tmp'),
							connect.static('test'),
							connect().use(
								'/bower_components',
								connect.static('./bower_components')
							),
							connect.static(appConfig.app)
						];
					}
				}
			},
			dist: {
				options: {
					open: true,
					base: '<%= birda.dist %>'
				}
			}
		},

		// Make sure there are no obvious mistakes
		jshint: {
			options: {
				jshintrc: '.jshintrc',
				reporter: require('jshint-stylish')
			},
			all: {
				src: [
					'Gruntfile.js',
					'<%= birda.app %>/scripts/{,*/}*.js'
				]
			},
			test: {
				options: {
					jshintrc: 'test/.jshintrc'
				},
				src: ['test/spec/{,*/}*.js']
			}
		},

		// Make sure code styles are up to par
		jscs: {
			options: {
				config: '.jscsrc',
				verbose: true
			},
			all: {
				src: [
					'Gruntfile.js',
					'<%= birda.app %>/scripts/{,*/}*.js'
				]
			},
			test: {
				src: ['test/spec/{,*/}*.js']
			}
		},

		// Empties folders to start fresh
		clean: {
			dist: {
				files: [{
					dot: true,
					src: [
						'.tmp',
						'<%= birda.dist %>/{,*/}*',
						'!<%= birda.dist %>/.git{,*/}*'
					]
				}]
			},
			server: '.tmp'
		},

		// Add vendor prefixed styles
		postcss: {
			options: {
				processors: [
					require('autoprefixer-core')({browsers: ['last 1 version']})
				]
			},
			server: {
				options: {
					map: true
				},
				files: [{
					expand: true,
					cwd: '.tmp/styles/',
					src: '{,*/}*.css',
					dest: '.tmp/styles/'
				}]
			},
			dist: {
				files: [{
					expand: true,
					cwd: '.tmp/styles/',
					src: '{,*/}*.css',
					dest: '.tmp/styles/'
				}]
			}
		},

		// Automatically inject Bower components into the app
		wiredep: {
			app: {
				src: ['<%= birda.app %>/index.html'],
				ignorePath:	/\.\.\//
			},
			test: {
				devDependencies: true,
				src: '<%= karma.unit.configFile %>',
				ignorePath:	/\.\.\//,
				fileTypes:{
					js: {
						block: /(([\s\t]*)\/{2}\s*?bower:\s*?(\S*))(\n|\r|.)*?(\/{2}\s*endbower)/gi,
							detect: {
								js: /'(.*\.js)'/gi
							},
							replace: {
								js: '\'{{filePath}}\','
							}
						}
					}
			},
			sass: {
				src: ['<%= birda.app %>/styles/{,*/}*.{scss,sass}'],
				ignorePath: /(\.\.\/){1,2}bower_components\//
			}
		},

		// Compiles Sass to CSS and generates necessary files if requested
		compass: {
			options: {
				sassDir: '<%= birda.app %>/styles',
				cssDir: '.tmp/styles',
				generatedImagesDir: '.tmp/images/generated',
				imagesDir: '<%= birda.app %>/images',
				javascriptsDir: '<%= birda.app %>/scripts',
				fontsDir: '<%= birda.app %>/styles/fonts',
				importPath: './bower_components',
				httpImagesPath: '/images',
				httpGeneratedImagesPath: '/images/generated',
				httpFontsPath: '/styles/fonts',
				relativeAssets: false,
				assetCacheBuster: false,
				raw: 'Sass::Script::Number.precision = 10\n'
			},
			dist: {
				options: {
					generatedImagesDir: '<%= birda.dist %>/images/generated'
				}
			},
			server: {
				options: {
					sourcemap: true
				}
			}
		},

		// Renames files for browser caching purposes
		filerev: {
			dist: {
				src: [
					'<%= birda.dist %>/scripts/{,*/}*.js',
					'<%= birda.dist %>/styles/{,*/}*.css',
					'<%= birda.dist %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
					'<%= birda.dist %>/styles/fonts/*'
				]
			}
		},

		// Reads HTML for usemin blocks to enable smart builds that automatically
		// concat, minify and revision files. Creates configurations in memory so
		// additional tasks can operate on them
		useminPrepare: {
			html: '<%= birda.app %>/index.html',
			options: {
				dest: '<%= birda.dist %>',
				flow: {
					html: {
						steps: {
							js: ['concat', 'uglifyjs'],
							css: ['cssmin']
						},
						post: {}
					}
				}
			}
		},

		// Performs rewrites based on filerev and the useminPrepare configuration
		usemin: {
			html: ['<%= birda.dist %>/{,*/}*.html'],
			css: ['<%= birda.dist %>/styles/{,*/}*.css'],
			js: ['<%= birda.dist %>/scripts/{,*/}*.js'],
			options: {
				assetsDirs: [
					'<%= birda.dist %>',
					'<%= birda.dist %>/images',
					'<%= birda.dist %>/styles'
				],
				patterns: {
					js: [[/(images\/[^''""]*\.(png|jpg|jpeg|gif|webp|svg))/g, 'Replacing references to images']]
				}
			}
		},

		// The following *-min tasks will produce minified files in the dist folder
		// By default, your `index.html`'s <!-- Usemin block --> will take care of
		// minification. These next options are pre-configured if you do not wish
		// to use the Usemin blocks.
		// cssmin: {
		//	 dist: {
		//		 files: {
		//			 '<%= birda.dist %>/styles/main.css': [
		//				 '.tmp/styles/{,*/}*.css'
		//			 ]
		//		 }
		//	 }
		// },
		// uglify: {
		//	 dist: {
		//		 files: {
		//			 '<%= birda.dist %>/scripts/scripts.js': [
		//				 '<%= birda.dist %>/scripts/scripts.js'
		//			 ]
		//		 }
		//	 }
		// },
		// concat: {
		//	 dist: {}
		// },

		imagemin: {
			dist: {
				files: [{
					expand: true,
					cwd: '<%= birda.app %>/images',
					src: '{,*/}*.{png,jpg,jpeg,gif}',
					dest: '<%= birda.dist %>/images'
				}]
			}
		},

		svgmin: {
			dist: {
				files: [{
					expand: true,
					cwd: '<%= birda.app %>/images',
					src: '{,*/}*.svg',
					dest: '<%= birda.dist %>/images'
				}]
			}
		},

		htmlmin: {
			dist: {
				options: {
					collapseWhitespace: true,
					conservativeCollapse: true,
					collapseBooleanAttributes: true,
					removeCommentsFromCDATA: true
				},
				files: [{
					expand: true,
					cwd: '<%= birda.dist %>',
					src: ['*.html'],
					dest: '<%= birda.dist %>'
				}]
			}
		},

		ngtemplates: {
			dist: {
				options: {
					module: 'birdaApp',
					htmlmin: '<%= htmlmin.dist.options %>',
					usemin: 'scripts/scripts.js'
				},
				cwd: '<%= birda.app %>',
				src: 'views/{,*/}*.html',
				dest: '.tmp/templateCache.js'
			}
		},

		// ng-annotate tries to make the code safe for minification automatically
		// by using the Angular long form for dependency injection.
		ngAnnotate: {
			dist: {
				files: [{
					expand: true,
					cwd: '.tmp/concat/scripts',
					src: '*.js',
					dest: '.tmp/concat/scripts'
				}]
			}
		},

		// Replace Google CDN references
		cdnify: {
			dist: {
				html: ['<%= birda.dist %>/*.html']
			}
		},

		// Copies remaining files to places other tasks can use
		copy: {
			dist: {
				files: [{
					expand: true,
					dot: true,
					cwd: '<%= birda.app %>',
					dest: '<%= birda.dist %>',
					src: [
						'*.{ico,png,txt}',
						'*.html',
						'images/{,*/}*.{webp}',
						'styles/fonts/{,*/}*.*'
					]
				}, {
					expand: true,
					cwd: '.tmp/images',
					dest: '<%= birda.dist %>/images',
					src: ['generated/*']
				}, {
					expand: true,
					cwd: '.',
					src: 'bower_components/bootstrap-sass-official/assets/fonts/bootstrap/*',
					dest: '<%= birda.dist %>'
				}]
			},
			styles: {
				expand: true,
				cwd: '<%= birda.app %>/styles',
				dest: '.tmp/styles/',
				src: '{,*/}*.css'
			}
		},

		// Run some tasks in parallel to speed up the build process
		concurrent: {
			server: [
				'compass:server'
			],
			test: [
				'compass'
			],
			dist: [
				'compass:dist',
				'imagemin',
				'svgmin'
			]
		},

		// Test settings
		karma: {
			unit: {
				configFile: 'test/karma.conf.js',
				singleRun: true
			}
		}
	});


	grunt.registerTask('serve', 'Compile then start a connect web server', function (target) {
		if (target === 'dist') {
			return grunt.task.run(['build', 'connect:dist:keepalive']);
		}

		grunt.task.run([
			'clean:server',
			'wiredep',
			'concurrent:server',
			'postcss:server',
			'connect:livereload',
			'watch'
		]);
	});

	grunt.registerTask('server', 'DEPRECATED TASK. Use the "serve" task instead', function (target) {
		grunt.log.warn('The `server` task has been deprecated. Use `grunt serve` to start a server.');
		grunt.task.run(['serve:' + target]);
	});

	grunt.registerTask('test', [
		'clean:server',
		'wiredep',
		'concurrent:test',
		'postcss',
		'connect:test',
		'karma'
	]);

	grunt.registerTask('build', [
		'clean:dist',
		'wiredep',
		'useminPrepare',
		'concurrent:dist',
		'postcss',
		'ngtemplates',
		'concat',
		'ngAnnotate',
		'copy:dist',
		'cdnify',
		'cssmin',
		'uglify',
		'filerev',
		'usemin',
		'htmlmin'
	]);

	grunt.registerTask('default', [
		'newer:jshint',
		'newer:jscs',
		'test',
		'build'
	]);
};
