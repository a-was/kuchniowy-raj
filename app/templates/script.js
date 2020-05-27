
    var calculateComplexity = function (password) {
      var complexity = 0;
      
      var regExps = [ 
        /[a-z]/
        /[A-Z]/
        /[0-9]/
        /.{8}/
        /.{16}/
    
      ];
      
      regExps.forEach(function (regexp) {
        if (regexp.test(password)) {
          complexity++;
        }
      });
      
      return {
        value: complexity,
        max: regExps.length
      };
    };
     
    var checkPasswordStregth = function (password) {
      var progress = document.querySelector('#password1'),
          complexity = calculateComplexity(this.value); 
      
      progress.value = complexity.value;
      progress.max = complexity.max;
    };
    
    var input = document.querySelector('#password1');
    input.addEventListener('keyup', checkPasswordStregth);