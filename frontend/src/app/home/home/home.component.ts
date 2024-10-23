import { Component } from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { CallToActionBannerComponent } from '../../components/call-to-action-banner/call-to-action-banner.component';
import { SearchComponentComponent } from '../search-component/search-component.component';
import { EHS_BANNER_CONTENT } from '../../../dummy-ehs-banner';
import { MatSidenavModule } from '@angular/material/sidenav';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [HeaderComponent, CallToActionBannerComponent, MatSidenavModule, SearchComponentComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

  ehsContent = EHS_BANNER_CONTENT;

  }


