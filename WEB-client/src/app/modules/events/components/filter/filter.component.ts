import { Filter } from './../../../../models/filter';
import { EventsService } from './../../servises/events.service';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import * as _ from "lodash";

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {
  filterParam: Filter;
  filterForm: FormGroup;

  
    name = '';
    value: number = 0
  

  selectedTypes: [number];
  selectedCategories: [number];
  selectedPlaces: [number];

  types: any = [];
  categories: any = [];
  places: any = [];
  startsMin: string = '';
  startsMax: string = '';

  @Output() setParams = new EventEmitter<Filter>();

  constructor(private pageService: EventsService) { }

  loadTypes(){
    this.pageService.getTypes().subscribe(x => {
      x.forEach(type => {
        this.value = type.id;
        this.name = type.name;
        let filElem = {
          value: this.value,
          name: this.name
        }
        this.types.push(filElem);
      });
      console.log(this.types);
      this.createFormInputs()
    })
  }

  loadCateg(){
    this.pageService.getStack().subscribe(x => {
      x.forEach(category => {
        this.value = category.id;
        this.name = category.name;
        let filElem = {
          value: this.value,
          name: this.name
        }
        this.categories.push(filElem);
      })
      console.log(this.categories);
      this.createFormInputs()
    })
  }

  loadCities(){
    this.pageService.getCities().subscribe(x => {
      x.forEach(place => {
        this.value = place.id;
        this.name = place.name;
        let filElem = {
          value: this.value,
          name: this.name
        }
        this.places.push(filElem);
      })
      console.log(this.places);
      this.createFormInputs()
    })
  }

  ngOnInit(): void {
    this.loadTypes();
    this.loadCateg();
    this.loadCities();
  }

  createFormInputs(){
    if(this.types != [] && this.categories != [] && this.places != []){
      this.filterForm = new FormGroup({
        // startsAtMin: this.createTimespaceMin(this.startsMin),
        // startsAtMax: this.createTimespaceMax(this.startsMax),
        types: this.createTypes(this.types),
        categories: this.createCategories(this.categories),
        places: this.createPlaces(this.places),
      });
      this.getSelectedTypes();
      this.getSelectedCategories();
      this.getSelectedPlaces();
    }
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

  createPlaces(placesInputs){
    const arr = placesInputs.map(place => {
      return new FormControl(place.selected || false);
    });
    return new FormArray(arr);
  }

  createTimespaceMin(minInput){
    return new FormControl(minInput || false)
  }

  createTimespaceMax(maxInput){
    return new FormControl(maxInput || false)
  }

  getSelectedTypes(){
    this.selectedTypes = _.map(this.filterForm.controls.types['controls'], (type, i) => {
      console.log(type.id);
      return type.value && this.types[i].value;
    });
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

  getSelectedPlaces(){
    this.selectedPlaces = _.map(this.filterForm.controls.places['controls'], (place, i) => {
      return place.value && this.places[i].value;
    });
    this.getSelectedPlacesName();
  }

  getSelectedPlacesName(){
    this.selectedPlaces = _.filter(
      this.selectedPlaces,
      function(place) {
        if(place != false) {
          return place;
        }
      }
    )
  }

  onSubmit(){
    this.getSelectedTypes();
    this.getSelectedCategories();
    this.getSelectedPlaces();
    console.log(this.selectedTypes);
    console.log(this.selectedCategories);
    console.log(this.selectedPlaces);
    console.log(this.startsMin);
    console.log(this.startsMax)
    this.filterParam = new Filter;
    this.filterParam.starts_at_min = this.startsMin;
    this.filterParam.starts_at_max = this.startsMax;
    this.filterParam.types = this.selectedTypes;
    this.filterParam.categories = this.selectedCategories;
    this.filterParam.cities = this.selectedPlaces;
    this.setParams.emit(this.filterParam);
    console.log(this.filterParam);
    console.log(this.startsMax)
  }

}
