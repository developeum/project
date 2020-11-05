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

  params: Filter = null;
  num: number = 0;
  userId: string;
  events: EventFL[] = [];

  constructor(private pageService: EventsService, private router: Router) {
    
  }

  ngOnInit(): void {
    this.params = new Filter;
    this.loadClearEvents();
  }

  loadEvents(){
    this.events = [];
    this.pageService.getEvents(this.params.types, this.params.categories, this.params.cities, this.params.starts_at_min, this.params.starts_at_max).subscribe(x => {
      this.events = x;
      console.log(x)
    })
    .unsubscribe()
  }

  loadClearEvents(){
    this.pageService.getClearEvents()
    .subscribe(x => {
      this.events = x;
      console.log(x)
    })

  }

  navToEvent(id){
    this.router.navigateByUrl('/event/' + id)
  }

  setParams(params: Filter){
    this.params = params;
    console.log(this.params);
    this.loadEvents();
  }

  loadMore(){
    this.loadEvents();
  }

}
