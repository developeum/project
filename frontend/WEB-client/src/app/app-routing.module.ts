import { AuthGuard } from './core/guards/auth.guard';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  {
    path: 'home',
    loadChildren: () => import('../app/modules/home/home.module').then(m => m.HomeModule)
  },
  {
    path: 'auth',
    loadChildren: () => import('../app/modules/auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: 'user',
    loadChildren: () => import('../app/modules/personal/personal.module').then(m => m.PersonalModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'events',
    loadChildren: () => import('../app/modules/events/events.module').then(m => m.EventsModule)
  },
  {
    path: 'event/:id',
    loadChildren: () => import('../app/modules/event/event.module').then(m => m.EventModule)
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
