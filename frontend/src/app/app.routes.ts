import { Routes } from '@angular/router';
import { EhsComponent } from './health-services/ehs/ehs.component';
import { HomeComponent } from './home/home/home.component';
import { AlarmplanComponent } from './alarmplan/alarmplan/alarmplan.component';



export const routes: Routes = [

    { path: '', component: HomeComponent},
    { path: 'ehs', component: EhsComponent},
    { path: 'test', component: AlarmplanComponent},
    { path: '**', pathMatch: 'full', redirectTo: ''},

];
