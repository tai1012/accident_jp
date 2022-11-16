"use strict";(self.webpackChunkipysheet=self.webpackChunkipysheet||[]).push([[273],{5871:(e,t,o)=>{o.d(t,{q:()=>d});var n=o(2759),r=o(2876),a=o(6486),i=o(8657);class s{constructor(e){this.id=(0,n.uuid)(),this.code=e,this.execute_promise=new Promise(((e,t)=>{this.resolve=e,this.reject=t}))}}class l{constructor(){this.requests={},this.initialize()}execute(e){const t=new s(e);return this.requests[t.id]=t,this.worker.postMessage({id:t.id,code:t.code}),t.execute_promise}initialize(){const e=URL.createObjectURL(new Blob(["(",function(){const e=postMessage,t=addEventListener;(e=>{let t=this;const o=["Object","Function","Infinity","NaN","undefined","caches","TEMPORARY","PERSISTENT","Array","Boolean","Number","String","Symbol","Map","Math","Set"];do{Object.getOwnPropertyNames(t).forEach((e=>{-1===o.indexOf(e)&&delete t[e]})),t=Object.getPrototypeOf(t)}while(t!==Object.prototype)})(),t("message",(({data:t})=>{const o=new Function("",`return (${t.code}\n);`);e({id:t.id,result:o()},void 0)}))}.toString(),")()"],{type:"application/javascript"}));this.worker=new Worker(e),this.worker.onmessage=({data:e})=>{this.requests[e.id].resolve(e.result),delete this.requests[e.id]},this.worker.onerror=({message:e})=>{(0,a.forEach)(this.requests,(t=>{t.reject(e)})),this.requests={},this.worker.terminate(),this.initialize()},URL.revokeObjectURL(e)}}class d extends n.WidgetModel{defaults(){return Object.assign(Object.assign({},super.defaults()),{_model_name:"RendererModel",_model_module:"ipysheet",_model_module_version:i.F,name:"",code:""})}initialize(e,t){super.initialize(e,t),this.kernel=new l;const o=this;this.rendering_function=function(e,t,n,a,i,s,l){r.renderers.TextRenderer.apply(this,arguments),o.kernel.execute(`(${o.get("code")})(${s})`).then((e=>{Object.assign(t.style,e)}))},r.renderers.registerRenderer(this.get("name"),this.rendering_function)}}},8647:(e,t,o)=>{o.r(t),o.d(t,{CellRangeModel:()=>d,RendererModel:()=>l.q,SheetModel:()=>h,SheetView:()=>g});var n=o(2759),r=o(6486),a=o(8657),i=o(2876),s=o.n(i);var l=o(5871);o(1035),o(1105),o(9259),i.cellTypes.registerCellType("widget",{renderer:async function(e,t,o,n,r,a,i){if(!t.hasAttribute("ghost-table")&&i.widget_view){let e=i.widget_view.el;1==t.children.length&&t.children[0]==e||(t.innerHTML="",e&&(t.appendChild(e),i.widget_view.trigger("displayed")))}}});class d extends n.WidgetModel{defaults(){return Object.assign(Object.assign({},super.defaults()),{_model_name:"CellRangeModel",_model_module:"ipysheet",_model_module_version:a.F,value:null,row_start:1,column_start:1,row_end:1,column_end:1,type:null,name:null,style:{},renderer:null,read_only:!1,choice:null,squeeze_row:!0,squeeze_column:!0,transpose:!1,numeric_format:"0.000",date_format:"YYYY/MM/DD",time_format:"h:mm:ss a"})}}d.serializers=Object.assign(Object.assign({},n.WidgetModel.serializers),{value:{deserialize:n.unpack_models}});class h extends n.DOMWidgetModel{defaults(){return Object.assign(Object.assign({},super.defaults()),{_model_name:"SheetModel",_view_name:"SheetView",_model_module:"ipysheet",_view_module:"ipysheet",_model_module_version:a.F,_view_module_version:a.F,rows:3,columns:4,cells:[],named_cells:{},row_headers:!0,column_headers:!0,stretch_headers:"all",column_width:null,column_resizing:!0,row_resizing:!0,search_token:""})}initialize(e,t){super.initialize(e,t),this.data=[[]],this.update_data_grid(!1),this._updating_grid=!1,this.on("change:rows change:columns",this.update_data_grid,this),this.on("change:cells",this.on_change_cells,this),this.on("data_change",this.grid_to_cell,this),(0,r.each)(this.get("cells"),(e=>this.cell_bind(e))),this.cells_to_grid()}on_change_cells(){this._updating_grid=!0;try{let e=this.previous("cells"),t=this.get("cells");for(let o=0;o<t.length;o++){let n=t[o];(0,r.includes)(e,n)||this.cell_bind(n)}this.cells_to_grid()}finally{this._updating_grid=!1}this.grid_to_cell()}cell_bind(e){e.on_some_change(["value","style","type","renderer","read_only","choice","numeric_format","date_format","time_format"],(()=>{this.cells_to_grid()}))}cells_to_grid(){this.data=[[]],this.update_data_grid(!1),(0,r.each)(this.get("cells"),(e=>{this._cell_data_to_grid(e)})),this.trigger("data_change")}_cell_data_to_grid(e){e.get("value");for(let t=e.get("row_start");t<=e.get("row_end");t++)for(let o=e.get("column_start");o<=e.get("column_end");o++){let n=e.get("value"),a=t-e.get("row_start"),i=o-e.get("column_start");if(t>=this.data.length||o>=this.data[t].length)continue;let s=this.data[t][o];e.get("transpose")?(e.get("squeeze_column")||(n=n[i]),e.get("squeeze_row")||(n=n[a])):(e.get("squeeze_row")||(n=n[a]),e.get("squeeze_column")||(n=n[i])),null!=n&&(s.value=n),null!=e.get("type")&&(s.options.type=e.get("type")),null!=e.get("renderer")&&(s.options.renderer=e.get("renderer")),null!=e.get("read_only")&&(s.options.readOnly=e.get("read_only")),null!=e.get("choice")&&(s.options.source=e.get("choice")),e.get("numeric_format")&&"numeric"==e.get("type")&&(s.options.numericFormat={pattern:e.get("numeric_format")}),e.get("date_format")&&"date"==e.get("type")&&(s.options.correctFormat=!0,s.options.dateFormat=e.get("date_format")||s.options.dateFormat),e.get("time_format")&&"time"==e.get("type")&&(s.options.correctFormat=!0,s.options.timeFormat=e.get("time_format")||s.options.timeFormat),s.options.style=(0,r.extend)({},s.options.style,e.get("style"))}}grid_to_cell(){if(!this._updating_grid){this._updating_grid=!0;try{(0,r.each)(this.get("cells"),(e=>{let t=[];for(let o=e.get("row_start");o<=e.get("row_end");o++){let n=[];for(let t=e.get("column_start");t<=e.get("column_end");t++){if(o>=this.data.length||t>=this.data[o].length)continue;let e=this.data[o][t];n.push(e.value)}e.get("squeeze_column")&&(n=n[0]),t.push(n)}e.get("squeeze_row")&&(t=t[0]),e.get("transpose")?e.set("value",(0,r.unzip)(t)):e.set("value",t),e.save_changes()}))}finally{this._updating_grid=!1}}}update_data_grid(e=!0){let t=this.get("rows"),o=this.get("columns"),n=()=>({value:null,options:{}}),a=()=>(0,r.times)(this.get("columns"),n);if(t<this.data.length)this.data=this.data.slice(0,t);else if(t>this.data.length)for(let e=this.data.length;e<t;e++)this.data.push(a());for(let e=0;e<t;e++){let t=this.data[e];if(o<t.length)t=t.slice(0,o);else if(o>t.length)for(let e=t.length;e<o;e++)t.push({value:null,options:{}});this.data[e]=t}e&&this.trigger("data_change")}}function c(e,t){return(0,r.map)(e,(function(e){return(0,r.map)(e,(function(e){return e[t]}))}))}h.serializers=Object.assign(Object.assign({},n.DOMWidgetModel.serializers),{cells:{deserialize:n.unpack_models},data:{deserialize:n.unpack_models}}),s().renderers.registerRenderer("styled",(function(e,t,o,n,a,i,l){let d=l.original_renderer||l.type||"text",h=s().renderers.getRenderer(d);h.apply(this,arguments),(0,r.each)(l.style,(function(e,o){t.style[o]=e}))}));class g extends n.DOMWidgetView{render(){this.widget_views={},this.el.classList.add("handsontable"),this.el.classList.add("jupyter-widgets"),this.table_container=document.createElement("div"),this.el.appendChild(this.table_container),this._table_constructed=this.displayed.then((async()=>{this.hot=await this._build_table(),this.model.on("data_change",this.on_data_change,this),this.model.on("change:column_headers change:row_headers",this._update_hot_settings,this),this.model.on("change:stretch_headers change:column_width",this._update_hot_settings,this),this.model.on("change:column_resizing change:row_resizing",this._update_hot_settings,this),this.model.on("change:search_token",this._search,this),this._search()}))}processPhosphorMessage(e){this._processLuminoMessage(e,super.processPhosphorMessage)}processLuminoMessage(e){this._processLuminoMessage(e,super.processLuminoMessage)}_processLuminoMessage(e,t){switch(t.call(this,e),e.type){case"resize":case"after-show":this._table_constructed.then((()=>{this.hot.render(),this.hot._refreshBorders(null)}))}}async _build_widgets_views(){let e=this.model.data,t=e.length,o=e[0].length,r={};for(let n=0;n<t;n++)for(let t=0;t<o;t++){let o=[n,t].join();if(e[n][t]&&"widget"==e[n][t].options.type){let a=e[n][t].value,i=this.widget_views[o];i&&(i.model.cid==a.cid?r[o]=Promise.resolve(i):(i.remove(),i=null)),!i&&a&&(r[o]=this.create_child_view(a))}}for(let t in this.widget_views)if(this.widget_views.hasOwnProperty(t)){let[o,n]=String(t).split(",").map((e=>parseInt(e))),r=this.widget_views[t];e[o][n]&&e[o][n].value&&e[o][n].value.cid==r.model.cid||r.remove()}this.widget_views=await(0,n.resolvePromisesDict)(r)}async _build_table(){return await this._build_widgets_views(),new(s())(this.table_container,(0,r.extend)({data:this._get_cell_data(),rowHeaders:!0,colHeaders:!0,search:!0,columnSorting:{sortEmptyCells:!1,indicator:!0,headerAction:!0,compareFunctionFactory:this._compareFunctionFactory},cells:(e,t)=>this._cell(e,t),afterChange:(e,t)=>{this._on_change(e,t)},afterRemoveCol:(e,t)=>{this._on_change_grid(e,t)},afterRemoveRow:(e,t)=>{this._on_change_grid(e,t)}},this._hot_settings()))}_compareFunctionFactory(e,t){return function(t,o){let r,a;return"desc"==e?(r=t,a=o):(r=o,a=t),r instanceof n.WidgetModel&&(r=r.get("value")),a instanceof n.WidgetModel&&(a=a.get("value")),null==r||null==a?0:r<a?-1:r>a?1:0}}_update_hot_settings(){this.hot.updateSettings(this._hot_settings())}_hot_settings(){return{colHeaders:this.model.get("column_headers"),rowHeaders:this.model.get("row_headers"),stretchH:this.model.get("stretch_headers"),colWidths:this.model.get("column_width")||void 0,manualColumnResize:this.model.get("column_resizing"),manualRowResize:this.model.get("row_resizing")}}_search(e=!0,t=!1){let o=this.model.get("search_token");t&&""==o||(this.hot.getPlugin("search").query(o),e&&this.hot.render())}_get_cell_data(){return c(this.model.data,"value")}_cell(e,t){let o=this.model.data,n=(0,r.cloneDeep)(o[e][t].options);return e<o.length&&t<o[e].length||console.error("cell out of range"),null==n.type&&delete n.type,null==n.style&&delete n.style,null==n.source&&delete n.source,"renderer"in n&&(n.original_renderer=n.renderer),n.renderer="styled",this.widget_views[[e,t].join()]&&(n.widget_view=this.widget_views[[e,t].join()]),n}_on_change_grid(e,t){let o=this.hot.getSourceDataArray();this.model.set({rows:o.length,columns:o[0].length}),this.model.save_changes()}_on_change(e,t){if(void 0!==this.hot&&"loadData"!=t&&"ObserveChanges.change"!=t){if("alter"==t){let e=this.hot.getSourceDataArray();return this.model.set({rows:e.length,columns:e[0].length}),void this.model.save_changes()}!function(e,t){for(let o=0;o<Math.min(e.length,t.length);o++)for(let n=0;n<Math.min(e[o].length,t[o].length);n++)e[o][n].value=t[o][n]}(this.model.data,this.hot.getSourceDataArray()),this.model.trigger("data_change")}}on_data_change(){this._last_data_set=new Promise((async(e,t)=>{let o=c(this.model.data,"value"),n=o.length,r=o[0].length,a=this.hot.countRows(),i=this.hot.countCols();n>a&&this.hot.alter("insert_row",n-1,n-a),n<this.hot.countRows()&&this.hot.alter("remove_row",n-1,a-n),r>i&&this.hot.alter("insert_col",r-1,r-i),r<i&&this.hot.alter("remove_col",r-1,i-r),await this._build_widgets_views(),this.hot.loadData(o),this.hot.updateSettings({colHeaders:!0,rowHeaders:!0}),this.hot.updateSettings({colHeaders:this.model.get("column_headers"),rowHeaders:this.model.get("row_headers")}),this._search(!1,!0),this.hot.render(),e(void 0)}))}set_cell(e,t,o){this.hot.setDataAtCell(e,t,o)}get_cell(e,t){return this.hot.getDataAtCell(e,t)}}},8657:(e,t,o)=>{o.d(t,{F:()=>r,i:()=>n});let n=o(4147).i8,r="~"+n},1150:(e,t,o)=>{o.d(t,{Z:()=>s});var n=o(8081),r=o.n(n),a=o(3645),i=o.n(a)()(r());i.push([e.id,"/* handsontable layout*/\n\n/* These properties can be overridden with the Layout widget.\n *\n *  - overflow: hidden;\n *   the first parent element with defined dimension and overflow: hidden is considered as the container for the spreadsheet\n *\n *  - height: 250px;\n *   we used a fixed value in pixels for the the natural height because `auto` yields a zero-height table in the Jupyter notebook.\n *\n */\n .handsontable.jupyter-widgets {\n    overflow: hidden;\n    height: 250px;\n }\n \n /* handsontable theme */\n .p-Widget .handsontable .table caption + thead tr:first-child th,\n .p-Widget .handsontable .table caption + thead tr:first-child td,\n .p-Widget .handsontable .table colgroup + thead tr:first-child th,\n .p-Widget .handsontable .table colgroup + thead tr:first-child td,\n .p-Widget .handsontable .table thead:first-child tr:first-child th,\n .p-Widget .handsontable .table thead:first-child tr:first-child td {\n   border-top: 1px solid var(--jp-border-color1);\n }\n \n .p-Widget .handsontable .table-bordered th:first-child,\n .p-Widget .handsontable .table-bordered td:first-child {\n   border-left: 1px solid var(--jp-border-color1);\n }\n \n .p-Widget .handsontable tr {\n   background-color: var(--jp-layout-color0);\n }\n \n .p-Widget .handsontable .table-striped > tbody > tr:nth-of-type(even) {\n   background-color: var(--jp-layout-color0);\n }\n \n .p-Widget .handsontable th,\n .p-Widget .handsontable td {\n   background-color: var(--jp-layout-color0);\n   color: var(--jp-content-font-color0);\n   font-size: var(--jp-ui-font-size1);\n   font-family: var(--jp-ui-font-family);\n   border-right: 1px solid var(--jp-border-color2);\n   border-bottom: 1px solid var(--jp-border-color2);\n }\n \n .p-Widget .handsontable td.htInvalid {\n   background-color: var(--jp-error-color0) !important; /*gives priority over td.area selection background*/\n }\n \n .p-Widget .handsontable th:last-child {\n   border-right: 1px solid var(--jp-border-color2);\n   border-bottom: 1px solid var(--jp-border-color2);\n }\n \n .p-Widget .handsontable tr:first-child th.htNoFrame,\n .p-Widget .handsontable th:first-child.htNoFrame,\n .p-Widget .handsontable th.htNoFrame {\n   background-color: var(--jp-layout-color0);\n }\n \n .p-Widget .handsontable th {\n   background-color: var(--jp-layout-color2);\n   color: var(--jp-content-font-color0);\n }\n \n .p-Widget .handsontable th.active {\n   background-color: var(--jp-layout-color3);\n }\n \n .p-Widget .handsontable .manualColumnResizer:hover,\n .p-Widget .handsontable .manualColumnResizer.active,\n .p-Widget .handsontable .manualRowResizer:hover,\n .p-Widget .handsontable .manualRowResizer.active {\n   background-color: var(--jp-brand-color1);\n }\n \n .p-Widget .handsontable .manualColumnResizerGuide {\n   background-color: var(--jp-brand-color1);\n }\n \n .p-Widget .handsontable .manualRowResizerGuide {\n   background-color: var(--jp-brand-color1);\n }\n \n .p-Widget .handsontable td.area:before,\n .p-Widget .handsontable td.area-1:before,\n .p-Widget .handsontable td.area-2:before,\n .p-Widget .handsontable td.area-3:before,\n .p-Widget .handsontable td.area-4:before,\n .p-Widget .handsontable td.area-5:before,\n .p-Widget .handsontable td.area-6:before,\n .p-Widget .handsontable td.area-7:before {\n   background-color: var(--jp-brand-color2);\n }\n \n .p-Widget .handsontable tbody th.ht__highlight,\n .p-Widget .handsontable thead th.ht__highlight {\n   background-color: var(--jp-layout-color3);\n }\n \n .p-Widget .handsontable tbody th.ht__active_highlight,\n .p-Widget .handsontable thead th.ht__active_highlight {\n   background-color: var(--jp-brand-color1);\n   color: white;\n }\n \n .p-Widget .handsontableInput {\n   box-shadow: 0 0 0 2px var(--jp-brand-color0) inset;\n   color: var(--jp-content-font-color0);\n   background-color: var(--jp-layout-color0);\n }\n \n .p-Widget .handsontable.listbox .ht_master table {\n   border: 1px solid var(--jp-border-color2);\n   background-color: var(--jp-layout-color0);\n }\n \n .p-Widget .handsontable.listbox tr td.current,\n .p-Widget .handsontable.listbox tr:hover td {\n   background-color: var(--jp-layout-color1);\n }\n \n .p-Widget .handsontable td.htSearchResult {\n   background: var(--jp-accent-color1);\n   color: white;\n }\n \n .p-Widget .htBordered.htTopBorderSolid {\n   border-top-color: var(--jp-border-color2);\n }\n .p-Widget .htBordered.htRightBorderSolid {\n   border-right-color: var(--jp-border-color2);\n }\n .p-Widget .htBordered.htBottomBorderSolid {\n   border-bottom-color: var(--jp-border-color2);\n }\n .p-Widget .htBordered.htLeftBorderSolid {\n   border-left-color: var(--jp-border-color2);\n }\n \n .p-Widget .handsontable tbody tr th:nth-last-child(2) {\n   border-right: 1px solid var(--jp-border-color2);\n }\n \n .p-Widget .handsontable thead tr:nth-last-child(2) th.htGroupIndicatorContainer {\n   border-bottom: 1px solid var(--jp-border-color2);\n }\n \n .p-Widget .ht_clone_top_left_corner thead tr th:nth-last-child(2) {\n   border-right: 1px solid var(--jp-border-color2);\n }\n \n .p-Widget .handsontable .wtBorder.current {\n   background-color: var(--jp-brand-color0) !important;\n   border-color: var(--jp-layout-color0) !important;\n }\n \n .p-Widget .handsontable .wtBorder.area {\n   background-color: var(--jp-brand-color0) !important;\n   border-color: var(--jp-layout-color0) !important;\n }\n \n /* Pikaday styling */\n .pika-single {\n     color: var(--jp-content-font-color0);\n     background: var(--jp-layout-color0);\n     border: 1px solid var(--jp-border-color2);\n     border-bottom-color: var(--jp-border-color2);\n     font-family: var(--jp-ui-font-family);\n }\n \n .pika-label {\n     background-color: var(--jp-layout-color0);\n }\n \n .pika-table th {\n     color: var(--jp-content-font-color1);\n }\n \n .pika-button {\n     color: var(--jp-content-font-color2);\n     background: var(--jp-layout-color2);\n }\n \n .pika-week {\n     font-size: var(--jp-ui-font-size1);\n     color: var(--jp-content-font-color1);\n }\n \n .is-today .pika-button {\n     color: var(--jp-content-font-color2);\n }\n \n .is-selected .pika-button {\n     color: var(--jp-layout-color0);\n     background: var(--jp-layout-color2);\n     box-shadow: inset 0 1px 3px var(--jp-brand-color0)\n }\n \n .is-inrange .pika-button {\n     background: var(--jp-brand-color1)\n }\n \n .is-startrange .pika-button {\n     color: var(--jp-layout-color0);\n     background: var(--jp-layout-color2);\n }\n \n .is-endrange .pika-button {\n     color: var(--jp-layout-color0);\n     background: var(--jp-layout-color2);\n }\n \n .is-disabled .pika-button,\n .is-outside-current-month .pika-button {\n     color: var(--jp-content-font-color1);\n }\n \n .pika-button:hover {\n     color: var(--jp-layout-color0);\n     background: var(--jp-layout-color2);\n }\n \n .pika-prev,\n .pika-next {\n     background-color: var(--jp-layout-color2);\n }\n ",""]);const s=i},9259:(e,t,o)=>{var n=o(3379),r=o.n(n),a=o(7795),i=o.n(a),s=o(569),l=o.n(s),d=o(3565),h=o.n(d),c=o(9216),g=o.n(c),u=o(4589),p=o.n(u),_=o(1150),A={};A.styleTagTransform=p(),A.setAttributes=h(),A.insert=l().bind(null,"head"),A.domAPI=i(),A.insertStyleElement=g(),r()(_.Z,A),_.Z&&_.Z.locals&&_.Z.locals},4333:e=>{e.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAYAAAAsEj5rAAAAU0lEQVR42u3VOwoAMAgE0dwfAnNjU26bYkBCFGwfiL9VVWoO+BJ4Gf3gtsEKKoFBNTCoCAYVwaAiGNQGMUHMkjGbgjk2mIONuXo0nC8XnCf1JXgArVIZAQh5TKYAAAAASUVORK5CYII="},168:e=>{e.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAYAAAAsEj5rAAAAUklEQVR42u3VMQoAIBADQf8Pgj+OD9hG2CtONJB2ymQkKe0HbwAP0xucDiQWARITIDEBEnMgMQ8S8+AqBIl6kKgHiXqQqAeJepBo/z38J/U0uAHlaBkBl9I4GwAAAABJRU5ErkJggg=="},1276:e=>{e.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAoCAMAAADJ7yrpAAAAKlBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKE86IAAAADXRSTlMABBEmRGprlJW72e77tTkTKwAAAFJJREFUeAHtzjkSgCAQRNFmQYUZ7n9dKUvru0TmvPAn3br0QfgdZ5xx6x+rQn23GqTYnq1FDcnuzZIO2WmedVqIRVxgGKEyjNgYRjKGkZ1hFIZ3I70LyM0VtU8AAAAASUVORK5CYII="},3525:e=>{e.exports="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAoCAMAAADJ7yrpAAAAKlBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKE86IAAAADXRSTlMABBEmRGprlJW72e77tTkTKwAAAFNJREFUeAHtzjkSgCAUBNHPgsoy97+ulGXRqJE5L+xkxoYt2UdsLb5bqFINz+aLuuLn5rIu2RkO3fZpWENimNgiw6iBYRTPMLJjGFxQZ1hxxb/xBI1qC8k39CdKAAAAAElFTkSuQmCC"},4147:e=>{e.exports={i8:"0.6.0"}}}]);