import { Routes } from '@angular/router';
import { EhsComponent } from './health-services/ehs/ehs.component';
import { HomeComponent } from './home/home/home.component';
import { SearchComponentComponent } from './home/search-component/search-component.component';
import { SubmittableFormCardComponent } from './components/submittable-form-card/submittable-form-card.component';
import { TestFormComponent } from './health-services/test-form/test-form.component';


export const routes: Routes = [

    { path: '', component: HomeComponent},
    { path: 'ehs', component: EhsComponent},
    { path: 'test', component: TestFormComponent},
    { path: '**', pathMatch: 'full', redirectTo: ''},

];
