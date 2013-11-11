module.exports = function(config){
    config.set({
    basePath : '../',

    files : [
      'token_checklist/static/lib/angular/angular.js',
      'token_checklist/static/lib/angular/angular-*.js',
      'tests/js/lib/angular/angular-mocks.js',
      'token_checklist/static/js/**/*.js',
      'tests/js/unit/**/*.js'
    ],

    exclude : [
      'token_checklist/static/lib/angular/angular-loader.js',
      'token_checklist/static/lib/angular/*.min.js',
      'token_checklist/static/lib/angular/angular-scenario.js'
    ],

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Chrome'],

    plugins : [
            'karma-junit-reporter',
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine'
            ],

    junitReporter : {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }

})};
