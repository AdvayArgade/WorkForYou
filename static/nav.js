var main=document.querySelector('main')
if(main.offsetHeight>=500){
    document.getElementsByTagName('footer')[0].style.position='relative';

}
if(main.offsetHeight<500){
    document.getElementsByTagName('footer')[0].style.position='fixed';

}