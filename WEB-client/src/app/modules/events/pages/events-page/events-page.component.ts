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

  params: any;
  num: number = 0;
  userId: string;
  events: EventFL[];

  constructor(private pageService: EventsService) {
    
  }

  ngOnInit(): void {
  }

  loadRandEvents(){
    this.pageService.getEvents().subscribe(x => {
      this.events = x;
    })
  }

  loadRecEvents(){
    this.pageService.getRec(this.userId).subscribe(x => {
      this.events = x;
    })
  }

  setParams(params: Filter){
    this.params = params;
    console.log(this.params);
  }

  loadMore(){

  }

}
