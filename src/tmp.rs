use nix::errno::Errno;
use std::env;
use std::ffi::OsString;
use std::fs;
use std::os::unix::ffi::OsStringExt;
use std::path::{Path, PathBuf};

pub struct TempDir {
    name: Option<PathBuf>,
}

impl TempDir {
    pub fn path(&self) -> &Path {
        self.name.as_ref().unwrap()
    }
}

pub fn tempdir() -> nix::Result<TempDir> {
    let mut template = env::temp_dir();
    template.push("nix-build-shell.XXXXXX");
    let mut bytes = template.into_os_string().into_vec();
    // null byte
    bytes.push(0);
    let res = unsafe { libc::mkdtemp(bytes.as_mut_ptr().cast()) };
    if res.is_null() {
        Err(nix::Error::Sys(Errno::last()))
    } else {
        // remove null byte
        bytes.pop();
        let name = PathBuf::from(OsString::from_vec(bytes));
        Ok(TempDir { name: Some(name) })
    }
}

impl Drop for TempDir {
    fn drop(&mut self) {
        if let Some(ref p) = self.name {
            let _ = fs::remove_dir_all(p);
        }
    }
}
