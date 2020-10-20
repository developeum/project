import { EventsService } from './../../servises/events.service';
import { EventFL } from './../../../../models/eventsFL';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-events-list',
  templateUrl: './events-list.component.html',
  styleUrls: ['./events-list.component.scss']
})
export class EventsListComponent implements OnInit {
  userId: string;
  events: EventFL[];

  constructor(private pageService: EventsService) { }

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

}
