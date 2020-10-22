import { Filter } from './../../../../models/filter';
import { EventsService } from './../../servises/events.service';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormArray, FormControl, FormGroup } from '@angular/forms';
import * as _ from "lodash";

@Component({
  selector: 'app-filter',
  templateUrl: './filter.component.html',
  styleUrls: ['./filter.component.scss']
})
export class FilterComponent implements OnInit {
  filterParam: Filter;
  filterForm: FormGroup;

  filElem: {
    name: string,
    value: number,
  };

  selectedTypes: [number];
  selectedCategories: [number];
  selectedPlaces: [number];

  types: any = [];
  categories: any = [];
  places: any = [];
  startsMin = new FormControl('');
  startsMax = new FormControl('');

  @Output() setParams = new EventEmitter<Filter>();

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

  loadCities(){
    this.pageService.getCities().subscribe(x => {
      x.forEach(place => {
        this.filElem.value = place.id;
        this.filElem.name = place.name;
        this.places.push(this.filElem);
      })
    })
  }

  ngOnInit(): void {
    this.loadTypes();
    this.loadCateg();
    this.loadCities();
    this.createFormInputs();
  }

  createFormInputs(){
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
    this.filterParam = new Filter;
    this.filterParam.starts_at_min = this.startsMin.value;
    this.filterParam.starts_at_max = this.startsMax.value;
    this.filterParam.types = this.selectedTypes;
    this.filterParam.categories = this.selectedCategories;
    this.filterParam.cities = this.selectedPlaces;
    this.setParams.emit(this.filterParam);
    console.log(this.filterParam);
    console.log(this.startsMax)
  }

}
