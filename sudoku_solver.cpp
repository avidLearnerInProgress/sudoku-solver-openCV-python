#include<bits/stdc++.h>
using namespace std;

int mod=1e9+7;
#define F(a,b,var) for(int var=a;var<b;var++)
#define FAST_INP  ios_base::sync_with_stdio(false);cin.tie(NULL)
#define EMPTY 0
#define N 9


//--------------------------------------Helpers-------------------------------------------

//Find cells containing 0
bool findEmptyCells(int grid[N][N], int &r, int &c){
    
    for(r=0 ; r<N; r++){
        for(c=0; c<N; c++){
            if(grid[r][c] == EMPTY)
                return true;
        }
    }
    return false;
}

//For specified row, find if any of enteries contain n
bool findMatchingInRow(int grid[N][N], int r, int n){
    
    int c;
    for(c=0; c<N; c++)
        if(grid[r][c] == n)
            return true;
    return false;
}

//For specified column, find if any of enteries contain n
bool findMatchingInCol(int grid[N][N], int c, int n){
    
    int r;
    for(r=0; r<N; r++)
        if(grid[r][c] == n)
            return true;
    return false;
}

//For each 3x3 sub-section in 9x9 grid, check enteries containing n
bool findMatchingInBox(int grid[N][N], int bStartRow, int bStartCol, int n){
    
    int r,c;
    for(r=0; r<3; r++)
        for(c=0; c<3; c++)
            if(grid[r + bStartRow][c + bStartCol] == n)
                return true;
    return false;
}


bool isSafe(int grid[N][N], int r, int c, int n){
    return !findMatchingInRow(grid, r, n) && !findMatchingInCol(grid, c, n) && !findMatchingInBox(grid, r-r%3, c-c%3, n);
}


//print grid
void printGrid(int grid[N][N]){
    int r,c;
    
    F(0, N, r){
        F(0, N, c)
            cout<<grid[r][c]<<" ";
        cout<<"\n";
    }
}

//---------------------------------------driver functions-------------------------------------------
bool solveSudoku(int grid[N][N]){
    int row, col;
    
    if(!findEmptyCells(grid, row, col))
        return true;
    
    for(int n=1; n<=9; n++){
        if(isSafe(grid, row, col, n)){
           grid[row][col] = n;
           
            if(solveSudoku(grid) == true)
                return true;
           
            grid[row][col] = EMPTY;
        }
    }
    
    return false;
}

//main function
int main()
{
    FAST_INP;
    //int T;
    //cin>>T;
    //while(T--){ 
    
    int grid[N][N] = {{3, 0, 6, 5, 0, 8, 4, 0, 0},
                      {5, 2, 0, 0, 0, 0, 0, 0, 0},
                      {0, 8, 7, 0, 0, 0, 0, 3, 1},
                      {0, 0, 3, 0, 1, 0, 0, 8, 0},
                      {9, 0, 0, 8, 6, 3, 0, 0, 5},
                      {0, 5, 0, 0, 9, 0, 6, 0, 0},
                      {1, 3, 0, 0, 0, 0, 2, 5, 0},
                      {0, 0, 0, 0, 0, 0, 0, 7, 4},
                      {0, 0, 5, 2, 0, 6, 3, 0, 0}};
    
    if(solveSudoku(grid) == true)
        printGrid(grid);
    else
        cout<<"Unable to solve!";

    //}
	return 0;
}





