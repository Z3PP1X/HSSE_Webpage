import { Component, input } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { CallToActionBanner } from './CallToActionBanner.model';

@Component({
  selector: 'app-call-to-action-banner',
  standalone: true,
  imports: [MatCardModule, MatButtonModule,],
  templateUrl: './call-to-action-banner.component.html',
  styleUrl: './call-to-action-banner.component.scss'
})
export class CallToActionBannerComponent {

  inputContent = input.required<CallToActionBanner[]>(); 

  



}
