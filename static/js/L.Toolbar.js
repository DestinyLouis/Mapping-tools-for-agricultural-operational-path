import CMButton from './L.Controls';

L.Control.CMButton = CMButton;

const Toolbar = L.Class.extend({
    options:{
        position: 'topleft',

    },

    initialize(map){
        this.init(map);
    },

    reinit(){
        this.addControls();
    },

    init(map){
        this.map = map;
        this.buttons = {};
        this.customContainer = L.DomUtil.create(
            'div',
            'leaflet-toolbar leaflet-custom leaflet-bar leaflet-control'
        );
        this._defineButtons();
    },

    getButtons(){
        return this.buttons;
    };

    addControls(options = this.options){
        L.Util.setOptions(this, options);
        this.applyIconStyle();
    },

    applyIconStyle(){
        const buttons = this.getButtons();

        const iconClasses = {
            customIcon: {
                drawMarker: '',
                drawPloyLine: '',
                //drawCurve: '',
                //editMarker: '',
                //editPloyLine: '',

            },
        };

        for(const name in buttons){
            const button = buttons[name];

            L.Util.setOptions(
                buttons,
                {className: iconClasses.customIcons[name]},
             );
        }
    },
});

export default Toolbar;