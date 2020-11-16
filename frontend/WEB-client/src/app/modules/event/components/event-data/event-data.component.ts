import { Observable } from 'rxjs';
import { Event } from './../../../../models/event';
import { EventService } from './../../services/event.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-event-data',
  templateUrl: './event-data.component.html',
  styleUrls: ['./event-data.component.scss']
})
export class EventDataComponent implements OnInit {

  eventData$: Observable<Event>
  imgToShow: any;
  isImageLoading: boolean = false;
  eventId: number;
  currentEvent: Event;

  constructor(private pageService: EventService, private route: ActivatedRoute) { 
    this.route.params.subscribe(params => {
      this.eventId = params["id"];
      setTimeout(this.internalVisited, 5000)
      
    })
  }

  ngOnInit(): void {
    this.loadEventInfo();
  }

  internalVisited(){
    this.pageService.postToVisited(this.eventId, "internal")
  }

  loadEventInfo(){
    this.eventData$ = this.pageService.getEventData(this.eventId)
    this.pageService.getEventData(this.eventId)
    .subscribe((event) => {
      this.currentEvent = event;
      console.log(this.currentEvent)
      this.loadImg(this.currentEvent.logo_path);
    })
  }

  onClick(){
    if(localStorage.getItem("currentUser") != null){
      this.pageService.postToVisited(this.eventId, "external")
      console.log(this.currentEvent.id)
    }
  }

  createImgFromBlob(image: Blob){
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imgToShow = reader.result;
    }, false);
    if(image){
      reader.readAsDataURL(image)
    }
  }

  loadImg(url: string) {
    this.isImageLoading = true;
    this.pageService.getEventImg(url).subscribe(data => {
      this.createImgFromBlob(data);
      this.isImageLoading = false;
    }, error => {
      this.isImageLoading = false;
      console.log(error)
    })
  }
}
