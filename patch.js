var fs = require('fs')
var _ = require('lodash')
var path = require('path')
var PythonShell = require('python-shell')

// check usage
if (process.argv.length < 5) {
  console.log('Usage: node patch.js ([SAVEFILE.sav] [#TRACKNUMBER] or [SONGFILE.srm|.lsdsng]) [SYNTH.snt] [#SYNTHNUMBER]')
  process.exit(1)
}

// create shell
var shell = new PythonShell('./lib/patcher.py', { args: process.argv.slice(2), pythonPath: 'python3' })

// log msgs
shell.on('message', function (msg) {
  // handle message (a line of text from stdout)
  console.log(msg)
})

// end
shell.end(function (err) {
  // error
  if (err) {
    console.log("Error : " + err)
    process.exit(1)
  }
  // done
  console.log('Done!')
})
