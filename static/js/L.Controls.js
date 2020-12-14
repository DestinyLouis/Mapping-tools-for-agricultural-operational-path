const CMButton = L.Control.extend({
                options: {
                    position: 'topleft',
                },
                initialize(options) {
                    this._button = Object.assign({}, this.options, options);
                },
                onAdd(map){//自定义控件按钮，需要重写onAdd()，说白了就是向网页中增加相对地图位置的标签，返回装有自定义按钮的container
                    this.map = map;
                    //生成工具栏标签，待写
                    this._container = this._map.Toolbar.customContainer;
                    //调用生成按钮子节点方法
                    this.buttonsDomNode = this._makeButton(this._button);
                    //容器加按钮容器标签，一个按钮容器中包含一个按钮标签，以及按下按下按钮后的展开内容
                    this._container.appendChild(this.buttonsDomNode);
                    return this._container;
                },
                toggle(e){//实现按钮的拨动开关效果
                    if(typeof e === 'boolean'){
                        //==只判断值，===判断值还判断数据类型，34=='34' t, 34==='34' f
                        this.button.toggleStatus = e;
                    }else{
                        this._button.toggleStatus = !this._button.toggleStatus;
                    }
                    this._applyStyleClasses();//向标签添加，删除class，实现按钮动态展开效果

                    return this._button.toggleStatus;//返回标签开关状态
                },
                toggled(){
                    return this._button.toggleStatus;
                },
                onCreate(){
                    this.toggle(false);
                },
                _triggerClick(e){
                    this._button.onClick(e, {button: this, event: e});
                    this._clicked(e);
                    this._button.afterClick(e, {button: this, event: e});
                },
                _makeButton(button){
                     //一个按钮容器包含一个active标签和一个按钮图标
                    //button container
                    const buttonContainer = L.DomUtil.create(
                        `div`,
                        `button-container`,
                        this._container
                    );

                    //button itself
                    const newButton = L.DomUtil.create(
                        `div`,
                        `leaflet-buttons-control-button`,
                        buttonContainer
                    );

                    //buttons active actions
                    const actionContainer = L.DomUtil.create(
                        `div`,
                        `leaflet-actions-container`,
                        buttonContainer
                    );
                    const activeActions = button.actions;

                    const actions = {
                        cancel: {
                            text: `取消`,
                            onClick(){
                                this._triggerClick();
                            },
                        },
                        finish: {
                            text: `结束`,
                            onClick(){
                                this._triggerClick();
                            },
                        },
                    };

                    activeActions.forEach(name => {
                        let action;
                        if(actions[name]){
                            action =actions[name];
                        }else if(name.text){
                            action = name;
                        }else{
                            return;
                        }
                        //生成点击后侧面展开的标签按钮
                        const actionNode = L.DomUtil.create(
                            `a`,
                            `leaflet-action action-${name}`,
                            actionContainer
                        );
                        //添加标签文字
                        actionNode.innerHTML = action.text;

                        //如果动作标签有点击事件，那么添加监听器到actionNode标签上
                        if(action.onClick){
                            L.DomEvent.addListener(actionNode, 'click', action.onClick, this);
                        }
                        //使actionNode的父标签点击事件失效
                        L.DomUtil.disableClickPropagation(actionNode);
                    });

                    //在按钮容器标签上添加active类
                    if(button.toggleStatus){
                        L.DomUtil.addClass(buttonContainer, 'active');
                    }

                    //添加按钮图标
                    const image = L.DomUtil.create(
                        `div`,
                        `control-icon`,
                        newButton
                    );
                    image.setAttribute('title', button.title);
                    image.setAttribute('src', button.iconUrl);
                    L.DomUtil.addClass(image, button.className);

                    //添加监听器给按钮，实现点击当前按钮，自动关闭其他按钮的开关效果
                    L.DomEvent.addListener(newButton, 'click', () =>{
                        if(this._button.disableOtherButtons){
                            this._map.Toolbar.triggerClickOnToggleButtons(this);
                        }
                    });



                    //添加点击出发事件到当前按钮
                    L.DomEvent.addListener(newButton, 'click', this._triggerClick, this);

                    //组织点击事件传播到父类，比如地图上
                    L.DomEvent.disableClickPropagate(newButton);
                    return buttonContainer;
                },

                //实现动态应用
                _applyStyleClasses(){
                    if(!this._container){
                        return;
                    }

                    if(!this._button.toggleStatus || this._button.cssToggle === false){
                        L.DomUtil.removeClass(this.buttonsDomNode, 'active');
                        L.DomUtil.removeClass(this._container, 'activeChild');
                    }else{
                        L.DomUtil.addClass(this.buttonsDomNode, 'active');
                        L.DomUtil.addClass(this._container, 'activeChild');
                    }
                },

                //点击按钮后触发
                _clicked(){
                    if(this_button.doToggle){
                        this.toggle();
                    }
                },
            });
            export default CMButton;