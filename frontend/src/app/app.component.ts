import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './home/header/header.component';
import { DUMMY_QUESTIONS } from '../dummy-questions';
import { DUMMY_QUESTIONS_ALT } from '../dummy-questions2';
import { EHS_BANNER_CONTENT } from '../dummy-ehs-banner';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CallToActionBannerComponent } from './components/call-to-action-banner/call-to-action-banner.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    HeaderComponent,
    MatCardModule,
    MatButtonModule,
    CallToActionBannerComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'frontend';

  appSidebar = false;

  ehsContent = EHS_BANNER_CONTENT;


}
