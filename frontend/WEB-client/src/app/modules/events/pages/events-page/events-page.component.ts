import { Router } from '@angular/router';

import { Component, OnInit } from '@angular/core';
import { EventFL } from 'src/app/models/eventsFL';
import { Filter } from 'src/app/models/filter';
import { EventsService } from '../../servises/events.service';

@Component({
  selector: 'app-events-page',
  templateUrl: './events-page.component.html',
  styleUrls: ['./events-page.component.scss']
})
export class EventsPageComponent implements OnInit {

  currSkip = 0;
  params: Filter = null;
  num: number = 0;
  userId: string;
  events: EventFL[] = [];
  filterState: boolean = false;
  visibility: boolean = true;
  filterChanged: boolean = false;

  constructor(private pageService: EventsService, private router: Router) {
    this.params = new Filter;
  }

  ngOnInit(): void {
    
    this.loadClearEvents();
  }

  loadEvents(){
    if(this.filterChanged){
      this.events = [];
    }
    this.pageService.getEvents(this.currSkip, this.params.types, this.params.categories, this.params.cities, this.params.starts_at_min, this.params.starts_at_max).subscribe(x => {
      x.forEach(event => {
        this.events.push(event)
        let dateTime = event.event_time.split('T');
        let russianDate = dateTime[0].split('-')
        event.event_time = russianDate[2] + '.' + russianDate[1] + '.' + russianDate[0];
      })
      this.events.forEach(event => {
        
      })
      console.log(x)
      console.log(this.params);
      console.log(this.currSkip)
    })
    this.filterChanged = false;
  }

  loadClearEvents(){
    this.pageService.getEvents(this.currSkip)
    .subscribe(x => {
      this.events = x;
      this.events.forEach(event => {
        let dateTime = event.event_time.split('T');
        let russianDate = dateTime[0].split('-')
        event.event_time = russianDate[2] + '.' + russianDate[1] + '.' + russianDate[0];
      })
      console.log(x)
    })
  }

  loadNextClearEvents(){
    this.pageService.getEvents(this.currSkip)
  }

  navToEvent(id){
    this.router.navigateByUrl('/event/' + id)
  }

  setParams(params: Filter){
    this.filterChanged = true;
    this.currSkip = 0;
    this.params = params;
    console.log(this.params);
    this.loadEvents();
    this.filterState = !this.filterState
  }

  loadMore(){
    this.currSkip += 10;
    if(this.params == null){
      this.loadNextClearEvents();
    }
    this.loadEvents();
  }

  onChanged(event: any){
    this.visibility = event;
    console.log(this.visibility)
  }

  changeFilterState(){
    this.filterState = !this.filterState;
  }
}
