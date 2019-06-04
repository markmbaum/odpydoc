
function arrange(){
    var nav_wrapper = document.getElementById('nav-wrapper');
    var nav = document.getElementById('nav');
    var main = document.getElementById('main');
    var body = document.body;
    var back = document.getElementById('up-module')

    var w_nav = nav.offsetWidth + 1;
    var m = w_nav.toString() + 'px';
    var w = (body.offsetWidth - w_nav).toString() + 'px';

    main.setAttribute('style', 'margin-left: ' + m);
    main.style.marginLeft = m;

    main.setAttribute('style', 'width: ' + w);
    main.style.width = w;

    console.log('arrange')
};

function toggleSource(obj){
    var parent = obj.parentElement;
    var children = parent.children;

    var header = children[0];
    var code = children[1];
    var codeDisplay = code.style.display;

    if(codeDisplay == 'block'){
        code.style.display = 'none';
        header.innerHTML = 'show source';
        parent.style.borderColor = '#383838'
    }else{
        code.style.display = 'block';
        header.innerHTML = 'hide source';
        parent.style.borderColor = '#C678DD'
    };

    arrange();
};
