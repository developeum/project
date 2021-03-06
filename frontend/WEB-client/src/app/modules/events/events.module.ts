import { GeneralModule } from './../../layout/components/general.module';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EventsPageComponent } from './pages/events-page/events-page.component';
import { EventsRoutingModule } from './events-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FilterComponent } from './components/filter/filter.component';
import { CalendarComponent } from './components/calendar/calendar.component';



@NgModule({
  declarations: [
    EventsPageComponent, 
    FilterComponent, CalendarComponent,
    
  ],
  imports: [
    CommonModule,
    EventsRoutingModule,
    GeneralModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class EventsModule { }
