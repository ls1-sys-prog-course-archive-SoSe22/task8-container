use std::env;
use std::path::PathBuf;

fn main() {
    let exe = env::current_exe().unwrap_or_else(|_| PathBuf::from(""));
    println!("Hello from {}. I got {} arguments", exe.display(), env::args().len());
}
