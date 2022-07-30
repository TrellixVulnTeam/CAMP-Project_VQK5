import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';
import { CampService } from '../camp.service';

@Component({
  selector: 'app-model',
  templateUrl: './model.component.html',
  styleUrls: ['./model.component.css']
})
export class ModelComponent implements OnInit {
  inputFields:any;
  inputFieldsGrouped:any;
  inputsList:any=[];
  outputData:any={};

  outputsList:any=[];
  outputFileds:any;

  loading: boolean = false;
  el: any;
  chartType: any = 'Line chart';
  
  errstatus:boolean = false;

  constructor(private service: CampService) { }

  ngOnInit(): void {
    this.loading = true;
    this.getInputFields();
    
  }


  
  /*************************************
          API Communicators
  **************************************/
  getInputFields(): void {
    this.service.getInputFields()
      .then((response) => response.json())
      .then(result => {
          this.inputFields = result;

          this.inputsList = [];
          for(var i in this.inputFields){
            this.inputFields[i].value = this.inputFields[i].default;
            this.inputFields[i].condition = JSON.parse(this.inputFields[i].condition);
            this.inputsList.push(this.inputFields[i].default);
          }
        
        this.getOutput();
        this.inputFieldsGrouped = this.groupBy(this.inputFields, 'inputgroup');
        this.inputFieldsGrouped = this.inputFieldsGrouped.__zone_symbol__value;
        
        for(var i in this.inputFieldsGrouped){
          this.inputFieldsGrouped[i]['items2'] = this.groupBy(this.inputFieldsGrouped[i]['items'], 'level0');
          this.inputFieldsGrouped[i]['items2'] = this.inputFieldsGrouped[i]['items2'].__zone_symbol__value;
          for(var j in this.inputFieldsGrouped[i]['items']){
            this.inputFieldsGrouped[i]['items3'] = this.groupBy(this.inputFieldsGrouped[i]['items'], 'header');
            this.inputFieldsGrouped[i]['items3'] = this.inputFieldsGrouped[i]['items3'].__zone_symbol__value;
          }
        }
        
    });
  }

  getOutputFields(): void {
    this.service.generateOutput()
    .then((response) => response.json())
    .then(result => {
        this.outputFileds = JSON.stringify(result);  
        alert(this.outputFileds)


        // this.outputsList = [];
        // for(var i in this.outputFileds){
        //   this.outputFileds[i].value = this.outputFileds[i].default;
        //   this.outputFileds[i].condition = JSON.parse(this.outputFileds[i].condition);
        //   this.outputsList.push(this.outputFileds[i].default);
        // }
  });

    
  
  }

  getOutput() {
    this.loading = true;
    this.outputData = [];
    this.service.setInputFields(this.inputsList)
        .then((response) => response.json())
        .then((result) => { 
          this.loading = false; 
          this.outputData = this.groupBy(result.data, 'group');     
          this.outputData = this.outputData["__zone_symbol__value"];     

    });
  }

  


  /*************************************
          Input/Output UI Helpers
  **************************************/

  async groupBy(data:any, key:any) {
    const helper:any = {};
    return data.reduce((groups:any,x:any) => {
      if (!helper[x[key]]) {
        helper[x[key]] = {
          group: x[key],
          items: [x],
          };

        groups.push(helper[x[key]]);

      } else { helper[x[key]].items.push(x); }
      
      return groups;
    }, []);
  }


  onInputChange(event: any, row:any) {
    if(row.type=="double"){
      this.errstatus=this.withinRange(row);
    }
    this.inputFields[row.id].value=event.target.value;
    this.inputsList[row.id]=event.target.value;
    this.inputFields[row.id].changed=true;
    this.getOutput();
  }
  
  withinRange(row:any){
    let max=row.condition.max[1];
    let min=row.condition.min[1];
      if (row.value<=min || row.value>=max){
        return true;
      }
    return false;
  }

  reset(){
    window.location.reload();
  }
  
 

}
