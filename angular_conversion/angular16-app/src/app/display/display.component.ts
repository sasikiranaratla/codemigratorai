
import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css'],
  standalone: true,
  imports: [CommonModule]
})
export class DisplayComponent implements OnInit {
  @Input() customer: string = '';

  constructor() { }

  ngOnInit(): void {
  }
}
