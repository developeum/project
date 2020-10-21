import { EventsService } from './../../servises/events.service';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import * as _ from "lodash";

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {
  filterForm: FormGroup;

  filElem: {
    name: string,
    value: number,
  };

  selectedTypes: [number];
  selectedCategories: [number];
  selectedFormat: [string];
  types: any = [];
  categories: any = [];

  constructor(private pageService: EventsService) { }

  loadTypes(){
    this.pageService.getTypes().subscribe(x => {
      x.forEach(type => {
        this.filElem.value = type.id;
        this.filElem.name = type.name;
        this.types.push(this.filElem);
      });
    })
  }

  loadCateg(){
    this.pageService.getStack().subscribe(x => {
      x.forEach(category => {
        this.filElem.value = category.id;
        this.filElem.name = category.name;
        this.categories.push(this.filElem);
      })
    })
  }

  ngOnInit(): void {
    this.loadTypes();
    this.loadCateg();
    this.createFormInputs();
  }

  createFormInputs(){
    this.filterForm = new FormGroup({
      types: this.createTypes(this.types),
      categories: this.createCategories(this.categories)
    });
    this.getSelectedTypes();
    this.getSelectedCategories();
  }

  createTypes(typesInputs){
    const arr = typesInputs.map(type => {
      return new FormControl(type.selected || false);
    });
    return new FormArray(arr);
  }

  createCategories(categoriesInputs){
    const arr = categoriesInputs.map(category => {
      return new FormControl(category.selected || false);
    });
    return new FormArray(arr);
  }

  getSelectedTypes(){
    this.selectedTypes = _.map(this.filterForm.controls.types['controls'], (type, i) => {
      console.log(type.id);
      return type.value && this.types[i].value;
    });
    console.log(this.selectedTypes)
    this.getSelectedTypesName();
  }

  getSelectedTypesName(){
    this.selectedTypes = _.filter(
      this.selectedTypes,
      function(type) {
        if(type != false) {
          return type;
        }
      }
    )
  }

  getSelectedCategories(){
    this.selectedCategories = _.map(this.filterForm.controls.categories['controls'], (category, i) => {
      return category.value && this.categories[i].value;
    });
    this.getSelectedCategoriesName()
  }

  getSelectedCategoriesName(){
    this.selectedCategories = _.filter(
      this.selectedCategories,
      function(category) {
        if(category != false) {
          return category
        }
      }
    )
  }

  onSubmit(){
    this.getSelectedTypes();
    console.log(this.selectedTypes)
  }

}
