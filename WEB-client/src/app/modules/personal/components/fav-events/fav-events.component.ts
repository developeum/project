import { EventFL } from './../../../../models/eventsFL';
import { Observable } from 'rxjs';
import { PersonalService } from './../../services/personal.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-fav-events',
  templateUrl: './fav-events.component.html',
  styleUrls: ['./fav-events.component.scss']
})
export class FavEventsComponent implements OnInit {
  favEvents$: Observable<EventFL[]>;

  constructor(private pageService: PersonalService) { }

  ngOnInit(): void {
    this.loadFavEvents();
  }

  loadFavEvents(){
    this.favEvents$ = this.pageService.getFavEvents();
  }

  loadMoreEvents(){
    
  }

}
