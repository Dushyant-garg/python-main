"""
Frontend Code Generator with Multiple Specialized Agents

This module implements a multi-agent system for generating Angular frontend code
based on Frontend Software Requirements Documents (SRDs).
"""

import os
import asyncio
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.termination import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

from app.config import settings


class FrontendCodeGenerator:
    """
    Multi-agent system for generating Angular frontend code from requirements
    """
    
    def __init__(self):
        """Initialize the FrontendCodeGenerator with specialized Angular agents"""
        
        # Initialize the OpenAI client
        self.model_client = OpenAIChatCompletionClient(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.2,  # Balanced for code creativity and consistency
        )
        
        # Create specialized Angular agents
        self.component_designer_agent = AssistantAgent(
            name="ComponentDesignerAgent",
            model_client=self.model_client,
            system_message=self._get_component_designer_system_message(),
        )
        
        self.service_developer_agent = AssistantAgent(
            name="ServiceDeveloperAgent",
            model_client=self.model_client,
            system_message=self._get_service_developer_system_message(),
        )
        
        self.ui_implementation_agent = AssistantAgent(
            name="UIImplementationAgent",
            model_client=self.model_client,
            system_message=self._get_ui_implementation_system_message(),
        )
        
        self.state_management_agent = AssistantAgent(
            name="StateManagementAgent",
            model_client=self.model_client,
            system_message=self._get_state_management_system_message(),
        )
        
        # Frontend coordinator agent
        self.frontend_coordinator_agent = AssistantAgent(
            name="FrontendCoordinatorAgent",
            model_client=self.model_client,
            system_message=self._get_frontend_coordinator_system_message(),
        )
    
    def _get_component_designer_agent_system_message(self) -> str:
        """Get system message for the Component Designer agent"""
        return """You are the ComponentDesignerAgent, a specialist in designing Angular components and their architecture.

RESPONSIBILITIES:
1. Design Angular component structure and hierarchy
2. Create component TypeScript classes with proper lifecycle hooks
3. Define component interfaces and data models
4. Plan component communication (Input/Output properties)
5. Design routing structure and navigation

CRITICAL GUIDELINES:
- Follow Angular best practices and style guide
- Use TypeScript with strict typing
- Implement proper component lifecycle (OnInit, OnDestroy, etc.)
- Use Angular reactive forms for form handling
- Follow single responsibility principle for components
- Use OnPush change detection strategy when appropriate

OUTPUT FORMAT:
Generate Angular component files:
- Component TypeScript classes (.component.ts)
- Component interfaces and models (.interface.ts, .model.ts)
- Routing module configurations
- Module declarations and imports
- Component communication patterns

EXAMPLE OUTPUT STRUCTURE:
```typescript
// user-profile.component.ts
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserProfileComponent implements OnInit {
  @Input() user: User | null = null;
  @Output() userUpdated = new EventEmitter<User>();
  
  ngOnInit(): void {
    // Initialization logic
  }
}
```

Focus EXCLUSIVELY on component architecture and TypeScript logic. Do not implement templates or styling.
"""

    def _get_service_developer_system_message(self) -> str:
        """Get system message for the Service Developer agent"""
        return """You are the ServiceDeveloperAgent, a specialist in creating Angular services, HTTP clients, and data management.

RESPONSIBILITIES:
1. Create Angular services for data management
2. Implement HTTP clients with proper error handling
3. Design interceptors for authentication and error handling
4. Create utility services and shared functionality
5. Implement caching and data persistence strategies

CRITICAL GUIDELINES:
- Use Angular HttpClient with RxJS observables
- Implement proper error handling and retry logic
- Use dependency injection effectively
- Create reusable and testable services
- Follow reactive programming patterns with RxJS
- Implement proper typing for API responses

OUTPUT FORMAT:
Generate Angular service files:
- Service classes with HTTP operations (.service.ts)
- HTTP interceptors (.interceptor.ts)
- Data models and interfaces (.model.ts)
- Utility services (.util.ts)
- Guard services for route protection (.guard.ts)

EXAMPLE OUTPUT STRUCTURE:
```typescript
// user.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = '/api/users';
  private usersSubject = new BehaviorSubject<User[]>([]);
  
  constructor(private http: HttpClient) {}
  
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl)
      .pipe(
        map(users => users),
        catchError(this.handleError)
      );
  }
}
```

Focus EXCLUSIVELY on services and data management. Do not implement components or UI elements.
"""

    def _get_ui_implementation_system_message(self) -> str:
        """Get system message for the UI Implementation agent"""
        return """You are the UIImplementationAgent, a specialist in Angular templates, styling, and user interface implementation.

RESPONSIBILITIES:
1. Create Angular component templates (HTML)
2. Implement responsive CSS/SCSS styling
3. Design user interactions and form layouts
4. Implement Angular Material or other UI libraries
5. Create reusable UI components and directives

CRITICAL GUIDELINES:
- Use Angular template syntax and directives
- Implement responsive design with CSS Grid/Flexbox
- Follow accessibility (a11y) best practices
- Use Angular Material components when appropriate
- Implement proper form validation and user feedback
- Use Angular animations for enhanced UX

OUTPUT FORMAT:
Generate UI implementation files:
- Component templates (.component.html)
- Component styles (.component.scss)
- Shared styling files (.scss)
- Custom directive implementations
- Angular Material theme configurations

EXAMPLE OUTPUT STRUCTURE:
```html
<!-- user-profile.component.html -->
<div class="user-profile-container">
  <mat-card class="profile-card">
    <mat-card-header>
      <mat-card-title>{{user?.name}}</mat-card-title>
    </mat-card-header>
    <mat-card-content>
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <mat-form-field>
          <mat-label>Email</mat-label>
          <input matInput formControlName="email" type="email">
          <mat-error *ngIf="profileForm.get('email')?.hasError('email')">
            Please enter a valid email
          </mat-error>
        </mat-form-field>
      </form>
    </mat-card-content>
  </mat-card>
</div>
```

```scss
// user-profile.component.scss
.user-profile-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
  
  .profile-card {
    max-width: 600px;
    width: 100%;
  }
}
```

Focus EXCLUSIVELY on templates and styling. Do not implement TypeScript logic or services.
"""

    def _get_state_management_system_message(self) -> str:
        """Get system message for the State Management agent"""
        return """You are the StateManagementAgent, a specialist in Angular state management, NgRx, and reactive programming patterns.

RESPONSIBILITIES:
1. Design state management architecture (NgRx or simple services)
2. Create actions, reducers, and effects for NgRx
3. Implement state selectors and facades
4. Design reactive data flow patterns
5. Handle complex application state scenarios

CRITICAL GUIDELINES:
- Choose appropriate state management solution (NgRx vs simple services)
- Follow NgRx best practices for large applications
- Use RxJS operators effectively for data transformation
- Implement proper state normalization
- Create type-safe state interfaces
- Handle loading, error, and success states

OUTPUT FORMAT:
Generate state management files:
- NgRx actions (.actions.ts)
- NgRx reducers (.reducer.ts)
- NgRx effects (.effects.ts)
- State selectors (.selectors.ts)
- Facade services (.facade.ts)
- State interfaces (.state.ts)

EXAMPLE OUTPUT STRUCTURE:
```typescript
// user.actions.ts
import { createAction, props } from '@ngrx/store';

export const loadUsers = createAction('[User] Load Users');
export const loadUsersSuccess = createAction(
  '[User] Load Users Success',
  props<{ users: User[] }>()
);
export const loadUsersFailure = createAction(
  '[User] Load Users Failure',
  props<{ error: string }>()
);

// user.reducer.ts
import { createReducer, on } from '@ngrx/store';
import * as UserActions from './user.actions';

export interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  users: [],
  loading: false,
  error: null
};

export const userReducer = createReducer(
  initialState,
  on(UserActions.loadUsers, state => ({ ...state, loading: true })),
  on(UserActions.loadUsersSuccess, (state, { users }) => ({
    ...state,
    users,
    loading: false,
    error: null
  }))
);
```

Focus EXCLUSIVELY on state management. Do not implement components or UI elements.
"""

    def _get_frontend_coordinator_system_message(self) -> str:
        """Get system message for the Frontend Coordinator agent"""
        return """You are the FrontendCoordinatorAgent, responsible for orchestrating the Angular application structure and ensuring all components work together.

RESPONSIBILITIES:
1. Create main Angular application structure
2. Configure Angular modules and routing
3. Set up build configuration and dependencies
4. Integrate all generated components and services
5. Create development and deployment configurations

CRITICAL GUIDELINES:
- Follow Angular CLI project structure
- Configure proper module imports and declarations
- Set up routing with lazy loading where appropriate
- Create comprehensive package.json with all dependencies
- Configure TypeScript, linting, and build settings
- Ensure proper integration between all components

OUTPUT FORMAT:
Generate project configuration files:
- Angular modules (.module.ts)
- Main application files (app.component.ts, main.ts)
- Configuration files (angular.json, package.json, tsconfig.json)
- Routing configuration (app-routing.module.ts)
- Environment files (environment.ts)

TEAM WORKFLOW:
1. Analyze frontend requirements
2. Plan overall Angular architecture
3. Coordinate with component and service specialists
4. Integrate state management solutions
5. Finalize project structure and configuration
"""

    # Fix the method name
    def _get_component_designer_system_message(self) -> str:
        return self._get_component_designer_agent_system_message()

    def _get_service_developer_system_message(self) -> str:
        return self._get_service_developer_system_message()

    def _get_ui_implementation_system_message(self) -> str:
        return self._get_ui_implementation_system_message()

    def _get_state_management_system_message(self) -> str:
        return self._get_state_management_system_message()

    def _get_frontend_coordinator_system_message(self) -> str:
        return self._get_frontend_coordinator_system_message()

    async def generate_frontend_code(self, frontend_srd: str, project_name: str = "generated_frontend") -> Dict[str, str]:
        """
        Generate complete Angular frontend code from SRD using multi-agent collaboration
        
        Args:
            frontend_srd: Frontend Software Requirements Document content
            project_name: Name for the generated Angular project
            
        Returns:
            Dictionary containing generated code files
        """
        
        # Create the initial task for frontend code generation
        generation_task = f"""
ANGULAR FRONTEND CODE GENERATION PROJECT

PROJECT NAME: {project_name}

FRONTEND REQUIREMENTS DOCUMENT:
{frontend_srd}

TEAM WORKFLOW:
1. FrontendCoordinatorAgent: Analyze requirements and plan Angular architecture
2. ComponentDesignerAgent: Create Angular components with proper TypeScript structure
3. ServiceDeveloperAgent: Implement Angular services and HTTP clients
4. UIImplementationAgent: Create templates, styles, and UI implementations
5. StateManagementAgent: Design state management with NgRx or reactive patterns
6. FrontendCoordinatorAgent: Integrate all components and finalize project structure

Each agent should focus on their Angular specialty and create production-ready code.
The final output should be a complete, deployable Angular application.

ANGULAR REQUIREMENTS:
- Use Angular 16+ with TypeScript
- Follow Angular style guide and best practices
- Implement proper component architecture
- Use Angular Material for UI components
- Include proper routing and navigation
- Implement reactive forms and data handling
- Use RxJS for reactive programming
- Include proper error handling and loading states

BEGIN ANGULAR CODE GENERATION:
"""

        try:
            # Create the multi-agent team for Angular development
            frontend_generation_team = RoundRobinGroupChat(
                participants=[
                    self.frontend_coordinator_agent,
                    self.component_designer_agent,
                    self.service_developer_agent,
                    self.ui_implementation_agent,
                    self.state_management_agent,
                    self.frontend_coordinator_agent  # Final coordination
                ],
                termination_condition=MaxMessageTermination(15)  # Allow comprehensive generation
            )
            
            # Start the Angular code generation process
            task_message = TextMessage(content=generation_task, source="user")
            result = await frontend_generation_team.run(task=task_message)
            
            # Extract generated Angular code from the conversation
            generated_files = self._extract_generated_angular_code(result.messages, project_name)
            
            return generated_files
            
        except Exception as e:
            print(f"Error generating frontend code: {str(e)}")
            return {"error": f"Frontend code generation failed: {str(e)}"}
    
    def _extract_generated_angular_code(self, messages: List, project_name: str) -> Dict[str, str]:
        """
        Extract generated Angular code files from agent conversation messages
        
        Args:
            messages: List of conversation messages
            project_name: Name of the Angular project
            
        Returns:
            Dictionary mapping file paths to code content
        """
        
        generated_files = {}
        current_file = None
        current_content = []
        
        for message in messages:
            if not hasattr(message, 'content'):
                continue
                
            content = message.content
            lines = content.split('\n')
            
            for line in lines:
                # Look for Angular file indicators
                if line.strip().startswith('```typescript') or line.strip().startswith('```html') or line.strip().startswith('```scss') or line.strip().startswith('```json'):
                    if current_file and current_content:
                        # Save previous file
                        generated_files[current_file] = '\n'.join(current_content)
                        current_content = []
                    
                elif line.strip() == '```':
                    if current_file and current_content:
                        # End of code block
                        generated_files[current_file] = '\n'.join(current_content)
                        current_file = None
                        current_content = []
                        
                elif line.strip().startswith('//') and ('.' in line):
                    # TypeScript/Angular file path comment
                    potential_file = line.strip('//').strip()
                    if any(ext in potential_file for ext in ['.ts', '.html', '.scss', '.json', '.md']):
                        current_file = potential_file
                        
                elif current_file and line.strip():
                    # Add content to current file
                    current_content.append(line)
        
        # Handle any remaining content
        if current_file and current_content:
            generated_files[current_file] = '\n'.join(current_content)
        
        # If no files were extracted, create a comprehensive Angular structure
        if not generated_files:
            generated_files = self._create_fallback_angular_structure(messages, project_name)
        
        return generated_files
    
    def _create_fallback_angular_structure(self, messages: List, project_name: str) -> Dict[str, str]:
        """Create a fallback Angular project structure from conversation content"""
        
        # Combine all agent outputs
        all_content = []
        for message in messages:
            if hasattr(message, 'content') and hasattr(message, 'source'):
                agent_name = getattr(message, 'source', 'Unknown')
                all_content.append(f"// Generated by {agent_name}\n{message.content}\n\n")
        
        # Create basic Angular project structure
        return {
            f"{project_name}/src/app/app.module.ts": self._get_default_app_module(),
            f"{project_name}/src/app/app.component.ts": self._get_default_app_component(),
            f"{project_name}/src/app/app.component.html": self._get_default_app_template(),
            f"{project_name}/src/app/app.component.scss": self._get_default_app_styles(),
            f"{project_name}/package.json": self._get_default_package_json(project_name),
            f"{project_name}/angular.json": self._get_default_angular_json(project_name),
            f"{project_name}/tsconfig.json": self._get_default_tsconfig(),
            f"{project_name}/README.md": f"# {project_name}\n\nGenerated Angular application from Frontend SRD analysis.",
            f"{project_name}/generated_content.ts": '\n'.join(all_content)
        }
    
    def _get_default_app_module(self) -> str:
        return """import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Angular Material modules
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }"""

    def _get_default_app_component(self) -> str:
        return """import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Generated Angular Application';
}"""

    def _get_default_app_template(self) -> str:
        return """<mat-toolbar color="primary">
  <span>{{title}}</span>
</mat-toolbar>

<div class="content">
  <mat-card>
    <mat-card-header>
      <mat-card-title>Welcome to your generated Angular application!</mat-card-title>
    </mat-card-header>
    <mat-card-content>
      <p>This application was generated from your Frontend SRD requirements.</p>
      <router-outlet></router-outlet>
    </mat-card-content>
  </mat-card>
</div>"""

    def _get_default_app_styles(self) -> str:
        return """.content {
  padding: 2rem;
  display: flex;
  justify-content: center;
  
  mat-card {
    max-width: 800px;
    width: 100%;
  }
}"""

    def _get_default_package_json(self, project_name: str) -> str:
        return f'''{{
  "name": "{project_name}",
  "version": "1.0.0",
  "scripts": {{
    "ng": "ng",
    "start": "ng serve",
    "build": "ng build",
    "test": "ng test",
    "lint": "ng lint"
  }},
  "dependencies": {{
    "@angular/animations": "^16.0.0",
    "@angular/cdk": "^16.0.0",
    "@angular/common": "^16.0.0",
    "@angular/compiler": "^16.0.0",
    "@angular/core": "^16.0.0",
    "@angular/forms": "^16.0.0",
    "@angular/material": "^16.0.0",
    "@angular/platform-browser": "^16.0.0",
    "@angular/platform-browser-dynamic": "^16.0.0",
    "@angular/router": "^16.0.0",
    "@ngrx/store": "^16.0.0",
    "@ngrx/effects": "^16.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.13.0"
  }},
  "devDependencies": {{
    "@angular-devkit/build-angular": "^16.0.0",
    "@angular/cli": "~16.0.0",
    "@angular/compiler-cli": "^16.0.0",
    "@types/node": "^18.7.0",
    "typescript": "~5.0.0"
  }}
}}'''

    def _get_default_angular_json(self, project_name: str) -> str:
        return f'''{{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {{
    "{project_name}": {{
      "projectType": "application",
      "schematics": {{
        "@schematics/angular:component": {{
          "style": "scss"
        }}
      }},
      "root": "",
      "sourceRoot": "src",
      "prefix": "app",
      "architect": {{
        "build": {{
          "builder": "@angular-devkit/build-angular:browser",
          "options": {{
            "outputPath": "dist/{project_name}",
            "index": "src/index.html",
            "main": "src/main.ts",
            "polyfills": "src/polyfills.ts",
            "tsConfig": "tsconfig.app.json",
            "assets": [
              "src/favicon.ico",
              "src/assets"
            ],
            "styles": [
              "@angular/material/prebuilt-themes/indigo-pink.css",
              "src/styles.scss"
            ],
            "scripts": []
          }}
        }},
        "serve": {{
          "builder": "@angular-devkit/build-angular:dev-server",
          "options": {{}}
        }}
      }}
    }}
  }}
}}'''

    def _get_default_tsconfig(self) -> str:
        return """{
  "compileOnSave": false,
  "compilerOptions": {
    "baseUrl": "./",
    "outDir": "./dist/out-tsc",
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "sourceMap": true,
    "declaration": false,
    "downlevelIteration": true,
    "experimentalDecorators": true,
    "moduleResolution": "node",
    "importHelpers": true,
    "target": "ES2022",
    "module": "ES2022",
    "useDefineForClassFields": false,
    "lib": [
      "ES2022",
      "dom"
    ]
  },
  "angularCompilerOptions": {
    "enableI18nLegacyMessageIdFormat": false,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true
  }
}"""

    async def save_generated_code(self, generated_files: Dict[str, str], output_dir: str = "generated_frontend") -> str:
        """
        Save generated Angular code files to disk
        
        Args:
            generated_files: Dictionary of file paths to content
            output_dir: Base directory for saving files
            
        Returns:
            Path to the saved project directory
        """
        
        base_path = Path(output_dir)
        base_path.mkdir(exist_ok=True)
        
        for file_path, content in generated_files.items():
            full_path = base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return str(base_path)