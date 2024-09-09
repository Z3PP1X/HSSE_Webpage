import { Component, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIcon, MatIconModule } from '@angular/material/icon';
import { SidebarService } from '../services/sidebar.service';
import { Injectable } from '@angular/core';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [MatButtonModule, MatIconModule,],
  providers: [SidebarService, Injectable],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {

  constructor(public sidebarService: SidebarService) {}

}
