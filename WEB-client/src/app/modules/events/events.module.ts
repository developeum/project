import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EventsPageComponent } from './pages/events-page/events-page.component';
import { EventsRoutingModule } from './events-routing.module';
import { EventsListComponent } from './components/events-list/events-list.component';
import { FilterComponent } from './components/filter/filter.component';



@NgModule({
  declarations: [EventsPageComponent, EventsListComponent, FilterComponent],
  imports: [
    CommonModule,
    EventsRoutingModule
  ]
})
export class EventsModule { }
